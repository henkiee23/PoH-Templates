/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.plan;

import java.util.Collections;
import java.util.List;

/**
 * Everything the outstanding steps of a plan will consume.
 */
public class ShoppingList
{
	private final List<ShoppingListEntry> entries;
	private final long coinCost;
	private final int highestLevelNeeded;

	ShoppingList(List<ShoppingListEntry> entries, long coinCost, int highestLevelNeeded)
	{
		this.entries = Collections.unmodifiableList(entries);
		this.coinCost = coinCost;
		this.highestLevelNeeded = highestLevelNeeded;
	}

	public List<ShoppingListEntry> getEntries()
	{
		return entries;
	}

	/**
	 * @return coins the estate agent will charge for the rooms still to be built
	 */
	public long getCoinCost()
	{
		return coinCost;
	}

	/**
	 * @return the highest Construction level any outstanding step needs
	 */
	public int getHighestLevelNeeded()
	{
		return highestLevelNeeded;
	}

	/**
	 * @return what the tradeable materials would cost at Grand Exchange prices, excluding
	 * {@link #getCoinCost()}
	 */
	public long getMaterialCost()
	{
		long total = 0;
		for (ShoppingListEntry entry : entries)
		{
			total += entry.getTotalPrice();
		}
		return total;
	}

	public long getTotalCost()
	{
		return getMaterialCost() + coinCost;
	}

	public boolean isEmpty()
	{
		return entries.isEmpty() && coinCost == 0;
	}
}
