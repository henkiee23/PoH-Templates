/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;


/**
 * A house style, which decides what the walls, floors and doors look like.
 */
public class HouseStyleDef
{
	private String id;
	private String name;
	/** Construction level required to use the style. */
	private int level;
	/** Coin cost charged by the estate agent to redecorate. */
	private int cost;
	private String note;

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

	public int getCost()
	{
		return cost;
	}

	public String getNote()
	{
		return note;
	}
}
