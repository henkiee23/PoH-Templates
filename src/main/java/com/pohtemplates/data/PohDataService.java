/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import com.google.gson.Gson;
import com.google.gson.JsonParseException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import javax.inject.Inject;
import javax.inject.Singleton;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Loads the bundled reference data once and hands it to the rest of the plugin.
 */
@Singleton
public class PohDataService
{
	private static final Logger log = LoggerFactory.getLogger(PohDataService.class);

	private static final String RESOURCE = "/com/pohtemplates/rooms.json";

	private final Gson gson;
	private PohData data;

	@Inject
	public PohDataService(Gson gson)
	{
		this.gson = gson;
	}

	/**
	 * @return the reference data, never {@code null}; an empty instance if the resource could not
	 * be read, so the panel can still show an error rather than the plugin failing to start
	 */
	public synchronized PohData get()
	{
		if (data == null)
		{
			data = load();
		}
		return data;
	}

	private PohData load()
	{
		try (InputStream in = PohDataService.class.getResourceAsStream(RESOURCE))
		{
			if (in == null)
			{
				log.warn("POH Templates data resource {} is missing", RESOURCE);
				return emptyData();
			}

			try (InputStreamReader reader = new InputStreamReader(in, StandardCharsets.UTF_8))
			{
				PohData loaded = gson.fromJson(reader, PohData.class);
				if (loaded == null)
				{
					return emptyData();
				}
				loaded.index();
				log.debug("Loaded {} rooms and {} items", loaded.getRooms().size(), loaded.getItems().size());
				return loaded;
			}
		}
		catch (IOException | JsonParseException e)
		{
			log.warn("Could not read POH Templates data", e);
			return emptyData();
		}
	}

	private static PohData emptyData()
	{
		PohData empty = new PohData();
		empty.index();
		return empty;
	}
}
