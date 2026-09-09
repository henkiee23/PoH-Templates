/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.model;

/**
 * The three levels a player-owned house can occupy.
 * <p>
 * {@link #getPlane()} is how a plan records the floor, and is part of the share-code format. It is
 * <b>not</b> the plane the floor occupies in the loaded scene: the house scene puts its ground floor
 * at plane 0, and the dungeon is a separate scene that also starts at plane 0.
 * {@code HouseScanner} works out which scene plane is which floor from the rooms standing on it.
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
