/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.data;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;

/**
 * The bundled reference data: house styles, rooms with their hotspots and buildable furniture, and
 * per-item acquisition notes.
 * <p>
 * Deserialised from {@code rooms.json}; {@link #index()} must be called once afterwards to build the
 * object-id lookups used by house detection.
 */
public class PohData
{
	private int format;
	private List<HouseStyleDef> styles;
	private List<RoomDef> rooms;
	private List<ItemInfo> items;

	private transient Map<String, RoomDef> roomsById = Collections.emptyMap();
	private transient Map<String, HouseStyleDef> stylesById = Collections.emptyMap();
	private transient Map<Integer, ItemInfo> itemsById = Collections.emptyMap();
	/**
	 * Object id to every meaning it can have. A few models are reused between rooms, so this is a
	 * list rather than a single value and callers decide between the candidates.
	 */
	private transient Map<Integer, List<ObjectRef>> objectRefs = Collections.emptyMap();

	public List<HouseStyleDef> getStyles()
	{
		return styles == null ? Collections.emptyList() : styles;
	}

	public List<RoomDef> getRooms()
	{
		return rooms == null ? Collections.emptyList() : rooms;
	}

	public List<ItemInfo> getItems()
	{
		return items == null ? Collections.emptyList() : items;
	}

	/**
	 * Builds the lookup tables. Safe to call more than once.
	 */
	public void index()
	{
		Map<String, RoomDef> roomIndex = new LinkedHashMap<>();
		for (RoomDef room : getRooms())
		{
			roomIndex.put(room.getId(), room);
		}
		roomsById = Collections.unmodifiableMap(roomIndex);

		Map<String, HouseStyleDef> styleIndex = new LinkedHashMap<>();
		for (HouseStyleDef style : getStyles())
		{
			styleIndex.put(style.getId(), style);
		}
		stylesById = Collections.unmodifiableMap(styleIndex);

		Map<Integer, ItemInfo> itemIndex = new HashMap<>();
		for (ItemInfo item : getItems())
		{
			itemIndex.put(item.getItemId(), item);
		}
		itemsById = Collections.unmodifiableMap(itemIndex);

		Map<Integer, List<ObjectRef>> objectIndex = new HashMap<>();
		for (RoomDef room : getRooms())
		{
			for (HotspotDef hotspot : room.getHotspots())
			{
				for (Integer objectId : hotspot.getObjectIds())
				{
					objectIndex.computeIfAbsent(objectId, k -> new ArrayList<>())
						.add(new ObjectRef(room, hotspot, null));
				}
				for (FurnitureDef furniture : hotspot.getOptions())
				{
					for (Integer objectId : furniture.getObjectIds())
					{
						objectIndex.computeIfAbsent(objectId, k -> new ArrayList<>())
							.add(new ObjectRef(room, hotspot, furniture));
					}
				}
			}
		}
		for (Map.Entry<Integer, List<ObjectRef>> entry : objectIndex.entrySet())
		{
			entry.setValue(Collections.unmodifiableList(entry.getValue()));
		}
		objectRefs = Collections.unmodifiableMap(objectIndex);
	}

	@Nullable
	public RoomDef getRoom(String roomId)
	{
		return roomId == null ? null : roomsById.get(roomId);
	}

	@Nullable
	public HouseStyleDef getStyle(String styleId)
	{
		return styleId == null ? null : stylesById.get(styleId);
	}

	@Nullable
	public ItemInfo getItem(int itemId)
	{
		return itemsById.get(itemId);
	}

	/**
	 * @return every room/hotspot the given scene object id could belong to, empty if it is not a
	 * house object this plugin knows about
	 */
	public List<ObjectRef> getObjectRefs(int objectId)
	{
		List<ObjectRef> refs = objectRefs.get(objectId);
		return refs == null ? Collections.emptyList() : refs;
	}

	public boolean isKnownObject(int objectId)
	{
		return objectRefs.containsKey(objectId);
	}

	public boolean isEmpty()
	{
		return getRooms().isEmpty();
	}

	public int getFormat()
	{
		return format;
	}
}
