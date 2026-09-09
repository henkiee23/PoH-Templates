/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import java.awt.Color;
import java.util.Collections;
import java.util.List;

/**
 * A room that can be placed on the house grid.
 */
public class RoomDef
{
	private String id;
	private String name;
	/** Construction level required to build the room itself. */
	private int level;
	/** Coin cost of building the room. */
	private int cost;
	/** Planes the room may be built on: 0 dungeon, 1 ground, 2 first floor. */
	private List<Integer> planes;
	/** Sides that have a door or opening in the unrotated room. */
	private List<Direction> doors;
	private List<HotspotDef> hotspots;
	/** Hex RGB used to tint the room in the grid editor, e.g. "#3E6B4F". */
	private String colour;
	private String note;

	public List<Integer> getPlanes()
	{
		return planes == null ? Collections.emptyList() : planes;
	}

	public List<Direction> getDoors()
	{
		return doors == null ? Collections.emptyList() : doors;
	}

	public List<HotspotDef> getHotspots()
	{
		return hotspots == null ? Collections.emptyList() : hotspots;
	}

	public boolean allowsPlane(int plane)
	{
		return getPlanes().contains(plane);
	}

	public HotspotDef getHotspot(String hotspotId)
	{
		if (hotspotId == null)
		{
			return null;
		}
		for (HotspotDef hotspot : getHotspots())
		{
			if (hotspotId.equals(hotspot.getId()))
			{
				return hotspot;
			}
		}
		return null;
	}

	/**
	 * @return the sides that have a door once the room is turned by {@code rotation} quarter turns
	 */
	public java.util.EnumSet<Direction> getDoors(int rotation)
	{
		java.util.EnumSet<Direction> rotated = java.util.EnumSet.noneOf(Direction.class);
		for (Direction door : getDoors())
		{
			rotated.add(door.rotate(rotation));
		}
		return rotated;
	}

	public Color toAwtColour()
	{
		if (colour == null || colour.isEmpty())
		{
			return new Color(0x5A5A5A);
		}
		try
		{
			return Color.decode(colour.startsWith("#") ? colour : "#" + colour);
		}
		catch (NumberFormatException e)
		{
			return new Color(0x5A5A5A);
		}
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

	public int getCost()
	{
		return cost;
	}

	public String getColour()
	{
		return colour;
	}

	public String getNote()
	{
		return note;
	}
}
