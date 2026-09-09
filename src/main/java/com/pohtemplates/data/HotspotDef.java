/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import java.util.Collections;
import java.util.List;

/**
 * A build slot inside a room, e.g. the larder space in a kitchen.
 */
public class HotspotDef
{
	private String id;
	private String name;
	/**
	 * Object ids the empty hotspot takes in the scene. A hotspot can have several because the game
	 * uses different models for the middle, side and corner variants of things like rugs.
	 */
	private List<Integer> objectIds;
	private List<FurnitureDef> options;

	public List<Integer> getObjectIds()
	{
		return objectIds == null ? Collections.emptyList() : objectIds;
	}

	public List<FurnitureDef> getOptions()
	{
		return options == null ? Collections.emptyList() : options;
	}

	public FurnitureDef getOption(String furnitureId)
	{
		if (furnitureId == null)
		{
			return null;
		}
		for (FurnitureDef option : getOptions())
		{
			if (furnitureId.equals(option.getId()))
			{
				return option;
			}
		}
		return null;
	}

	public String getId()
	{
		return id;
	}

	public String getName()
	{
		return name;
	}
}
