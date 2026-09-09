/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.model;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * A complete house plan: which room goes in which grid cell, how it is turned, and what is built in it.
 * <p>
 * Serialised directly to JSON for both on-disk storage and share codes, so field names are part of
 * the exchange format. Any breaking change must bump {@link #CURRENT_FORMAT} and be handled in
 * {@code com.pohtemplates.share.ShareCodec}.
 */
public class HouseTemplate
{
	/** Grid is 13x13 rooms; a house chunk is 8x8 tiles and the scene is 104x104. */
	public static final int GRID_SIZE = 13;
	public static final int CURRENT_FORMAT = 1;

	private int format = CURRENT_FORMAT;
	private String id = UUID.randomUUID().toString();
	private String name = "New plan";
	private String author = "";
	private String notes = "";
	/** Id of a house style in {@code rooms.json}, e.g. {@code basic_wood}. */
	private String style = "basic_wood";
	private List<PlannedRoom> rooms = new ArrayList<>();

	public HouseTemplate()
	{
	}

	public HouseTemplate(String name)
	{
		this.name = name;
	}

	public int getFormat()
	{
		return format;
	}

	public void setFormat(int format)
	{
		this.format = format;
	}

	public String getId()
	{
		return id;
	}

	public void setId(String id)
	{
		this.id = id;
	}

	public String getName()
	{
		return name;
	}

	public void setName(String name)
	{
		this.name = name;
	}

	public String getAuthor()
	{
		return author;
	}

	public void setAuthor(String author)
	{
		this.author = author;
	}

	public String getNotes()
	{
		return notes;
	}

	public void setNotes(String notes)
	{
		this.notes = notes;
	}

	public String getStyle()
	{
		return style;
	}

	public void setStyle(String style)
	{
		this.style = style;
	}

	public List<PlannedRoom> getRooms()
	{
		if (rooms == null)
		{
			rooms = new ArrayList<>();
		}
		return rooms;
	}

	public void setRooms(List<PlannedRoom> rooms)
	{
		this.rooms = rooms == null ? new ArrayList<>() : rooms;
	}

	public PlannedRoom getRoomAt(int plane, int x, int y)
	{
		for (PlannedRoom room : getRooms())
		{
			if (room.getPlane() == plane && room.getX() == x && room.getY() == y)
			{
				return room;
			}
		}
		return null;
	}

	/**
	 * Places {@code room}, replacing whatever occupied that cell.
	 */
	public void putRoom(PlannedRoom room)
	{
		removeRoomAt(room.getPlane(), room.getX(), room.getY());
		getRooms().add(room);
	}

	public boolean removeRoomAt(int plane, int x, int y)
	{
		return getRooms().removeIf(r -> r.getPlane() == plane && r.getX() == x && r.getY() == y);
	}

	public static boolean inBounds(int x, int y)
	{
		return x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE;
	}

	public HouseTemplate copy()
	{
		HouseTemplate copy = new HouseTemplate();
		copy.format = format;
		copy.id = id;
		copy.name = name;
		copy.author = author;
		copy.notes = notes;
		copy.style = style;
		copy.rooms = new ArrayList<>();
		for (PlannedRoom room : getRooms())
		{
			copy.rooms.add(room.copy());
		}
		return copy;
	}

	/**
	 * @return a copy with a fresh id, used when importing so an imported plan never silently
	 * overwrites one the user already has.
	 */
	public HouseTemplate copyWithNewId()
	{
		HouseTemplate copy = copy();
		copy.id = UUID.randomUUID().toString();
		return copy;
	}
}
