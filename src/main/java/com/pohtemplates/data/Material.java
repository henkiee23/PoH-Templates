/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;


/**
 * A quantity of one item consumed by building a piece of furniture.
 */
public class Material
{
	private int itemId;
	private int quantity;

	public Material()
	{
	}

	public Material(int itemId, int quantity)
	{
		this.itemId = itemId;
		this.quantity = quantity;
	}

	public int getItemId()
	{
		return itemId;
	}

	public int getQuantity()
	{
		return quantity;
	}
}
