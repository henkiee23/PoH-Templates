/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.model;

/**
 * The three levels a player-owned house can occupy.
 * <p>
 * The ordinal of each value is <b>not</b> significant; {@link #getPlane()} is the plane the level
 * occupies inside the house instance and is the value that matches {@code WorldView#getPlane()}.
 */
public enum HouseFloor
{
	DUNGEON(0, "Dungeon"),
	GROUND(1, "Ground floor"),
	UPPER(2, "First floor");

	private final int plane;
	private final String displayName;

	HouseFloor(int plane, String displayName)
	{
		this.plane = plane;
		this.displayName = displayName;
	}

	public int getPlane()
	{
		return plane;
	}

	public String getDisplayName()
	{
		return displayName;
	}

	/**
	 * @return the floor occupying {@code plane}, or {@code null} if the plane is not part of a house
	 */
	public static HouseFloor ofPlane(int plane)
	{
		for (HouseFloor floor : values())
		{
			if (floor.plane == plane)
			{
				return floor;
			}
		}
		return null;
	}

	@Override
	public String toString()
	{
		return displayName;
	}
}
