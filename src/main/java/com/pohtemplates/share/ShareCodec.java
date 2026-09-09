/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.share;

import com.google.gson.Gson;
import com.google.gson.JsonParseException;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Iterator;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
import javax.inject.Inject;
import javax.inject.Singleton;

/**
 * Turns a plan into a short text code and back.
 * <p>
 * The code is {@code POHT1-} followed by URL-safe base64 of the gzipped JSON of the plan. There is
 * no network access anywhere in this class: sharing is done by the user copying and pasting the
 * code. The accompanying website reads and writes the same format.
 * <p>
 * Decoding treats its input as hostile. The inflated size is capped so a maliciously crafted code
 * cannot exhaust memory, and the decoded plan is bounds-checked before it is handed back.
 */
@Singleton
public class ShareCodec
{
	private static final String PREFIX = "POHT1-";
	/** Codes are pasted by hand; anything larger than this is not a real plan. */
	private static final int MAX_CODE_CHARS = 200_000;
	/** Cap on the inflated JSON, to bound the work a hostile code can cause. */
	private static final int MAX_INFLATED_BYTES = 512 * 1024;
	private static final int MAX_ROOMS = HouseTemplate.GRID_SIZE * HouseTemplate.GRID_SIZE * 3;
	private static final int MAX_TEXT_FIELD_CHARS = 512;

	private final Gson gson;

	@Inject
	public ShareCodec(Gson gson)
	{
		this.gson = gson;
	}

	public String encode(HouseTemplate template) throws ShareCodeException
	{
		try
		{
			byte[] json = gson.toJson(template).getBytes(StandardCharsets.UTF_8);
			ByteArrayOutputStream compressed = new ByteArrayOutputStream();
			try (GZIPOutputStream gzip = new GZIPOutputStream(compressed))
			{
				gzip.write(json);
			}
			return PREFIX + Base64.getUrlEncoder().withoutPadding().encodeToString(compressed.toByteArray());
		}
		catch (IOException e)
		{
			throw new ShareCodeException("Could not build a share code for this plan.", e);
		}
	}

	public HouseTemplate decode(String code) throws ShareCodeException
	{
		if (code == null)
		{
			throw new ShareCodeException("No share code was given.");
		}

		String trimmed = code.trim();
		if (trimmed.isEmpty())
		{
			throw new ShareCodeException("No share code was given.");
		}
		if (trimmed.length() > MAX_CODE_CHARS)
		{
			throw new ShareCodeException("That share code is too long to be a house plan.");
		}
		if (!trimmed.startsWith(PREFIX))
		{
			throw new ShareCodeException("That does not look like a POH Templates code. Codes start with " + PREFIX);
		}

		// Whitespace creeps in when a code is pasted out of a chat client or a wrapped email.
		String payload = trimmed.substring(PREFIX.length()).replaceAll("\\s", "");

		byte[] compressed;
		try
		{
			compressed = Base64.getUrlDecoder().decode(payload);
		}
		catch (IllegalArgumentException e)
		{
			throw new ShareCodeException("That share code is damaged; try copying it again.", e);
		}

		String json = inflate(compressed);

		HouseTemplate template;
		try
		{
			template = gson.fromJson(json, HouseTemplate.class);
		}
		catch (JsonParseException e)
		{
			throw new ShareCodeException("That share code is damaged; try copying it again.", e);
		}

		if (template == null)
		{
			throw new ShareCodeException("That share code does not contain a house plan.");
		}
		if (template.getFormat() > HouseTemplate.CURRENT_FORMAT)
		{
			throw new ShareCodeException("That plan was made with a newer version of POH Templates. Update the plugin to open it.");
		}

		sanitise(template);
		return template;
	}

	private static String inflate(byte[] compressed) throws ShareCodeException
	{
		try (GZIPInputStream gzip = new GZIPInputStream(new ByteArrayInputStream(compressed)))
		{
			ByteArrayOutputStream out = new ByteArrayOutputStream();
			byte[] buffer = new byte[8192];
			int total = 0;
			int read;
			while ((read = gzip.read(buffer)) != -1)
			{
				total += read;
				if (total > MAX_INFLATED_BYTES)
				{
					throw new ShareCodeException("That share code unpacks to far more data than a house plan; ignoring it.");
				}
				out.write(buffer, 0, read);
			}
			return new String(out.toByteArray(), StandardCharsets.UTF_8);
		}
		catch (IOException e)
		{
			throw new ShareCodeException("That share code is damaged; try copying it again.", e);
		}
	}

	/**
	 * Drops anything a hand-edited or hostile code might contain that the rest of the plugin would
	 * not expect: out-of-range grid cells, absurd rotations and overlong text.
	 */
	private static void sanitise(HouseTemplate template) throws ShareCodeException
	{
		template.setName(clamp(template.getName(), "Imported plan"));
		template.setAuthor(clamp(template.getAuthor(), ""));
		template.setNotes(clamp(template.getNotes(), ""));

		if (template.getRooms().size() > MAX_ROOMS)
		{
			throw new ShareCodeException("That plan claims more rooms than a house can hold.");
		}

		Iterator<PlannedRoom> it = template.getRooms().iterator();
		while (it.hasNext())
		{
			PlannedRoom room = it.next();
			if (room == null
				|| room.getRoom() == null
				|| !HouseTemplate.inBounds(room.getX(), room.getY())
				|| room.getPlane() < 0
				|| room.getPlane() > 2)
			{
				it.remove();
				continue;
			}
			// Normalises into 0 - 3.
			room.setRotation(room.getRotation());
		}
	}

	private static String clamp(String value, String fallback)
	{
		if (value == null)
		{
			return fallback;
		}
		String stripped = value.replaceAll("[\\p{Cntrl}]", " ").trim();
		if (stripped.isEmpty())
		{
			return fallback;
		}
		return stripped.length() > MAX_TEXT_FIELD_CHARS
			? stripped.substring(0, MAX_TEXT_FIELD_CHARS)
			: stripped;
	}
}
