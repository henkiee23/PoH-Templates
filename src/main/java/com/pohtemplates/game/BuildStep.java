/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.game;

import com.pohtemplates.data.FurnitureDef;
import com.pohtemplates.data.HotspotDef;
import com.pohtemplates.data.Material;
import com.pohtemplates.data.RoomDef;
import java.util.Collections;
import java.util.List;
import javax.annotation.Nullable;

/**
 * One thing the player still has to do to turn their house into the plan.
 */
public class BuildStep
{
	public enum Type
	{
		/** The grid square is empty and the plan wants a room there. */
		ADD_ROOM,
		/** There is a room there, but not the one the plan asks for. */
		REPLACE_ROOM,
		/** The right room, turned the wrong way. */
		ROTATE_ROOM,
		/** The room is right; a hotspot inside it is empty or holds the wrong thing. */
		BUILD_FURNITURE
	}

	private final Type type;
	private final int plane;
	private final int x;
	private final int y;
	private final RoomDef room;
	private final int rotation;
	private final HotspotDef hotspot;
	private final FurnitureDef furniture;
	private final FurnitureDef existing;

	private BuildStep(Type type, int plane, int x, int y, RoomDef room, int rotation,
		@Nullable HotspotDef hotspot, @Nullable FurnitureDef furniture, @Nullable FurnitureDef existing)
	{
		this.type = type;
		this.plane = plane;
		this.x = x;
		this.y = y;
		this.room = room;
		this.rotation = rotation;
		this.hotspot = hotspot;
		this.furniture = furniture;
		this.existing = existing;
	}

	public static BuildStep room(Type type, int plane, int x, int y, RoomDef room, int rotation)
	{
		return new BuildStep(type, plane, x, y, room, rotation, null, null, null);
	}

	public static BuildStep furniture(int plane, int x, int y, RoomDef room, int rotation,
		HotspotDef hotspot, FurnitureDef furniture, @Nullable FurnitureDef existing)
	{
		return new BuildStep(Type.BUILD_FURNITURE, plane, x, y, room, rotation, hotspot, furniture, existing);
	}

	public Type getType()
	{
		return type;
	}

	public int getPlane()
	{
		return plane;
	}

	public int getX()
	{
		return x;
	}

	public int getY()
	{
		return y;
	}

	public RoomDef getRoom()
	{
		return room;
	}

	public int getRotation()
	{
		return rotation;
	}

	@Nullable
	public HotspotDef getHotspot()
	{
		return hotspot;
	}

	@Nullable
	public FurnitureDef getFurniture()
	{
		return furniture;
	}

	/**
	 * @return what is currently built in the hotspot, when the plan asks for something different
	 */
	@Nullable
	public FurnitureDef getExisting()
	{
		return existing;
	}

	/**
	 * @return the construction level this step needs
	 */
	public int getLevelRequired()
	{
		return furniture != null ? furniture.getLevel() : room.getLevel();
	}

	/**
	 * @return the items this step consumes; empty for a room, which costs only coins
	 */
	public List<Material> getMaterials()
	{
		return furniture != null ? furniture.getMaterials() : Collections.emptyList();
	}

	/**
	 * @return the coins this step costs: the estate agent's fee for a room, or the price of a
	 * furnishing that is bought outright rather than built from materials
	 */
	public int getCoinCost()
	{
		if (type == Type.ADD_ROOM || type == Type.REPLACE_ROOM)
		{
			return room.getCost();
		}
		return furniture == null ? 0 : furniture.getCoins();
	}

	public String describe()
	{
		switch (type)
		{
			case ADD_ROOM:
				return "Build " + room.getName();
			case REPLACE_ROOM:
				return "Replace with " + room.getName();
			case ROTATE_ROOM:
				return "Turn " + room.getName() + " to face " + rotationName(rotation);
			case BUILD_FURNITURE:
			default:
				if (furniture == null || hotspot == null)
				{
					return "Build furniture";
				}
				return existing == null
					? "Build " + furniture.getName() + " (" + hotspot.getName() + ")"
					: "Replace " + existing.getName() + " with " + furniture.getName();
		}
	}

	private static String rotationName(int rotation)
	{
		switch (((rotation % 4) + 4) % 4)
		{
			case 1:
				return "east";
			case 2:
				return "south";
			case 3:
				return "west";
			default:
				return "north";
		}
	}
}
