/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import javax.annotation.Nullable;

/**
 * What a scene object id means: the room it belongs to, the hotspot it fills, and, when the object
 * is built furniture rather than an empty hotspot, which furniture it is.
 */
public class ObjectRef
{
	private final RoomDef room;
	private final HotspotDef hotspot;
	private final FurnitureDef furniture;

	public ObjectRef(RoomDef room, HotspotDef hotspot, @Nullable FurnitureDef furniture)
	{
		this.room = room;
		this.hotspot = hotspot;
		this.furniture = furniture;
	}

	public RoomDef getRoom()
	{
		return room;
	}

	public HotspotDef getHotspot()
	{
		return hotspot;
	}

	/**
	 * @return the built furniture, or {@code null} when the object is an empty hotspot
	 */
	@Nullable
	public FurnitureDef getFurniture()
	{
		return furniture;
	}

	public boolean isEmptyHotspot()
	{
		return furniture == null;
	}
}
