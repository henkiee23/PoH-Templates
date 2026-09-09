/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.plan;

import java.util.Collections;
import java.util.List;

/**
 * One line of the shopping list: how many of an item the outstanding work needs, what it costs, and
 * how an ironman would get hold of it.
 */
public class ShoppingListEntry
{
	private final int itemId;
	private final String name;
	private final int quantity;
	private final int unitPrice;
	private final boolean tradeable;
	private final List<String> sources;

	ShoppingListEntry(int itemId, String name, int quantity, int unitPrice, boolean tradeable, List<String> sources)
	{
		this.itemId = itemId;
		this.name = name;
		this.quantity = quantity;
		this.unitPrice = unitPrice;
		this.tradeable = tradeable;
		this.sources = sources == null ? Collections.emptyList() : Collections.unmodifiableList(sources);
	}

	public int getItemId()
	{
		return itemId;
	}

	public String getName()
	{
		return name;
	}

	public int getQuantity()
	{
		return quantity;
	}

	/**
	 * @return the Grand Exchange price of one, or 0 when the item has no tradeable price
	 */
	public int getUnitPrice()
	{
		return unitPrice;
	}

	public long getTotalPrice()
	{
		return (long) unitPrice * quantity;
	}

	public boolean isTradeable()
	{
		return tradeable;
	}

	/**
	 * @return where to get this without the Grand Exchange, most convenient first
	 */
	public List<String> getSources()
	{
		return sources;
	}
}
