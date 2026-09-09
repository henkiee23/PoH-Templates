/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.store;

import com.google.gson.Gson;
import com.google.gson.JsonParseException;
import com.google.gson.reflect.TypeToken;
import com.pohtemplates.model.HouseTemplate;
import java.io.File;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import javax.annotation.Nullable;
import javax.inject.Inject;
import javax.inject.Singleton;
import net.runelite.client.RuneLite;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Keeps the user's plans in {@code .runelite/poh-templates/templates.json}.
 * <p>
 * Everything is held in memory; writes are pushed to the shared executor so no disk I/O happens on
 * the client thread or the Swing event thread.
 */
@Singleton
public class TemplateStore
{
	private static final Logger log = LoggerFactory.getLogger(TemplateStore.class);

	private static final Type LIST_TYPE = new TypeToken<List<HouseTemplate>>()
	{
	}.getType();

	private final Gson gson;
	private final ScheduledExecutorService executor;
	private final File directory;
	private final File file;

	private final List<HouseTemplate> templates = new ArrayList<>();
	private boolean loaded;

	@Inject
	public TemplateStore(Gson gson, ScheduledExecutorService executor)
	{
		this.gson = gson;
		this.executor = executor;
		this.directory = new File(RuneLite.RUNELITE_DIR, "poh-templates");
		this.file = new File(directory, "templates.json");
	}

	public synchronized List<HouseTemplate> getTemplates()
	{
		ensureLoaded();
		return Collections.unmodifiableList(new ArrayList<>(templates));
	}

	@Nullable
	public synchronized HouseTemplate get(String id)
	{
		ensureLoaded();
		for (HouseTemplate template : templates)
		{
			if (template.getId().equals(id))
			{
				return template;
			}
		}
		return null;
	}

	/**
	 * Adds a plan, or replaces the stored one with the same id.
	 */
	public synchronized void put(HouseTemplate template)
	{
		ensureLoaded();
		templates.removeIf(t -> t.getId().equals(template.getId()));
		templates.add(template);
		saveAsync();
	}

	public synchronized void remove(String id)
	{
		ensureLoaded();
		if (templates.removeIf(t -> t.getId().equals(id)))
		{
			saveAsync();
		}
	}

	public synchronized boolean isEmpty()
	{
		ensureLoaded();
		return templates.isEmpty();
	}

	private void ensureLoaded()
	{
		if (loaded)
		{
			return;
		}
		loaded = true;

		if (!file.exists())
		{
			return;
		}

		try (Reader reader = Files.newBufferedReader(file.toPath(), StandardCharsets.UTF_8))
		{
			List<HouseTemplate> read = gson.fromJson(reader, LIST_TYPE);
			if (read != null)
			{
				for (HouseTemplate template : read)
				{
					if (template != null && template.getId() != null)
					{
						templates.add(template);
					}
				}
			}
		}
		catch (IOException | JsonParseException e)
		{
			log.warn("Could not read saved house plans from {}", file, e);
		}
	}

	/**
	 * Writes the current plans to disk on the shared executor.
	 */
	public void saveAsync()
	{
		final String json;
		synchronized (this)
		{
			json = gson.toJson(templates, LIST_TYPE);
		}
		executor.execute(() -> write(json));
	}

	private void write(String json)
	{
		try
		{
			//noinspection ResultOfMethodCallIgnored
			directory.mkdirs();

			// Write beside the real file and move it into place, so an interrupted write cannot
			// leave the user with a half-written plan file.
			File temp = File.createTempFile("templates", ".json", directory);
			try (Writer writer = Files.newBufferedWriter(temp.toPath(), StandardCharsets.UTF_8))
			{
				writer.write(json);
			}
			try
			{
				Files.move(temp.toPath(), file.toPath(),
					StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
			}
			catch (AtomicMoveNotSupportedException e)
			{
				Files.move(temp.toPath(), file.toPath(), StandardCopyOption.REPLACE_EXISTING);
			}
		}
		catch (IOException e)
		{
			log.warn("Could not save house plans to {}", file, e);
		}
	}
}
