/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import java.util.Collections;
import java.util.List;

/**
 * One buildable option for a hotspot, e.g. "Oak larder" in the larder space.
 */
public class FurnitureDef
{
	private String id;
	private String name;
	/** Construction level required to build it. */
	private int level;
	/** Construction experience granted. */
	private double xp;
	/**
	 * Coins this costs on top of any materials. Dungeon guards, traps and oubliette floors are
	 * bought outright rather than built from items.
	 */
	private int coins;
	private List<Material> materials;
	/** Object ids this furniture takes in the scene once built, used for detection. */
	private List<Integer> objectIds;
	/** Free-text caveat shown in the UI, e.g. a quest requirement. */
	private String note;

	public List<Material> getMaterials()
	{
		return materials == null ? Collections.emptyList() : materials;
	}

	public List<Integer> getObjectIds()
	{
		return objectIds == null ? Collections.emptyList() : objectIds;
	}

	public String getId()
	{
		return id;
	}

	public String getName()
	{
		return name;
	}

	public int getLevel()
	{
		return level;
	}

	public double getXp()
	{
		return xp;
	}

	public int getCoins()
	{
		return coins;
	}

	public String getNote()
	{
		return note;
	}
}
