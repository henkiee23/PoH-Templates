/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import java.util.Collections;
import java.util.List;

/**
 * Static notes about a construction material: how a player gets hold of it.
 * <p>
 * Live prices are not stored here; they come from RuneLite's own item price cache at runtime.
 */
public class ItemInfo
{
	private int itemId;
	private String name;
	/** False for items the Grand Exchange cannot price, e.g. untradeables. */
	private boolean tradeable = true;
	/** Where a player without the Grand Exchange can get this, most convenient first. */
	private List<String> sources;

	public List<String> getSources()
	{
		return sources == null ? Collections.emptyList() : sources;
	}

	public int getItemId()
	{
		return itemId;
	}

	public String getName()
	{
		return name;
	}

	public boolean isTradeable()
	{
		return tradeable;
	}
}
