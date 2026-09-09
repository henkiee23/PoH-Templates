/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.model;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/**
 * One room placed on the house grid, together with the furniture the user intends to build in it.
 * <p>
 * This class is serialised directly to JSON, so field names are part of the share-code format and
 * must not be renamed without bumping {@link HouseTemplate#CURRENT_FORMAT}.
 */
public class PlannedRoom
{
	/** Plane the room sits on. See {@link HouseFloor#getPlane()}. */
	private int plane;
	/** Room grid coordinate, 0 - 12, west to east. */
	private int x;
	/** Room grid coordinate, 0 - 12, south to north. */
	private int y;
	/** Id of a room in {@code rooms.json}. */
	private String room;
	/** Room rotation in quarter turns clockwise, 0 - 3. */
	private int rotation;
	/** Hotspot id to furniture id. Absent entries mean "leave empty". */
	private Map<String, String> furniture = new LinkedHashMap<>();

	public PlannedRoom()
	{
	}

	public PlannedRoom(int plane, int x, int y, String room, int rotation)
	{
		this.plane = plane;
		this.x = x;
		this.y = y;
		this.room = room;
		this.rotation = rotation;
	}

	public int getPlane()
	{
		return plane;
	}

	public void setPlane(int plane)
	{
		this.plane = plane;
	}

	public int getX()
	{
		return x;
	}

	public void setX(int x)
	{
		this.x = x;
	}

	public int getY()
	{
		return y;
	}

	public void setY(int y)
	{
		this.y = y;
	}

	public String getRoom()
	{
		return room;
	}

	public void setRoom(String room)
	{
		this.room = room;
	}

	public int getRotation()
	{
		return rotation;
	}

	public void setRotation(int rotation)
	{
		this.rotation = ((rotation % 4) + 4) % 4;
	}

	public Map<String, String> getFurniture()
	{
		if (furniture == null)
		{
			furniture = new LinkedHashMap<>();
		}
		return furniture;
	}

	public void setFurniture(Map<String, String> furniture)
	{
		this.furniture = furniture == null ? new LinkedHashMap<>() : furniture;
	}

	public PlannedRoom copy()
	{
		PlannedRoom copy = new PlannedRoom(plane, x, y, room, rotation);
		copy.furniture = new LinkedHashMap<>(getFurniture());
		return copy;
	}

	@Override
	public boolean equals(Object o)
	{
		if (this == o)
		{
			return true;
		}
		if (!(o instanceof PlannedRoom))
		{
			return false;
		}
		PlannedRoom that = (PlannedRoom) o;
		return plane == that.plane
			&& x == that.x
			&& y == that.y
			&& rotation == that.rotation
			&& Objects.equals(room, that.room)
			&& Objects.equals(getFurniture(), that.getFurniture());
	}

	@Override
	public int hashCode()
	{
		return Objects.hash(plane, x, y, room, rotation, getFurniture());
	}

	@Override
	public String toString()
	{
		return "PlannedRoom{" + room + " @ " + plane + "/" + x + "," + y + " rot=" + rotation + '}';
	}
}
