/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

/**
 * A side of a room square, in the unrotated orientation used by the data files.
 * <p>
 * North is +y on the house grid, east is +x, matching OSRS world coordinates.
 */
public enum Direction
{
	NORTH(0, 1),
	EAST(1, 0),
	SOUTH(0, -1),
	WEST(-1, 0);

	private final int dx;
	private final int dy;

	Direction(int dx, int dy)
	{
		this.dx = dx;
		this.dy = dy;
	}

	public int getDx()
	{
		return dx;
	}

	public int getDy()
	{
		return dy;
	}

	public Direction opposite()
	{
		switch (this)
		{
			case NORTH:
				return SOUTH;
			case EAST:
				return WEST;
			case SOUTH:
				return NORTH;
			default:
				return EAST;
		}
	}

	/**
	 * Applies a room rotation.
	 *
	 * @param quarterTurnsClockwise 0 - 3
	 * @return the side this one ends up on once the room is turned
	 */
	public Direction rotate(int quarterTurnsClockwise)
	{
		Direction[] clockwise = {NORTH, EAST, SOUTH, WEST};
		int index = 0;
		for (int i = 0; i < clockwise.length; i++)
		{
			if (clockwise[i] == this)
			{
				index = i;
				break;
			}
		}
		int turns = ((quarterTurnsClockwise % 4) + 4) % 4;
		return clockwise[(index + turns) % clockwise.length];
	}
}
