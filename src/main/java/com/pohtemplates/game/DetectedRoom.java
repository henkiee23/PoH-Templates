/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.game;

import com.pohtemplates.data.FurnitureDef;
import com.pohtemplates.data.HotspotDef;
import com.pohtemplates.data.ObjectRef;
import com.pohtemplates.data.RoomDef;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;
import net.runelite.api.TileObject;

/**
 * One 8x8 chunk of the house as it currently stands, assembled from the objects the client has told
 * us about. Nothing here is read from the server directly; it is all derived from the loaded scene.
 */
public class DetectedRoom
{
	private final int plane;
	private final int x;
	private final int y;
	private int rotation;

	/** Object hash to what we saw there. Keyed by hash so respawns replace rather than duplicate. */
	private final Map<Long, Sighting> sightings = new HashMap<>();

	private RoomDef resolvedRoom;
	private boolean dirty = true;

	DetectedRoom(int plane, int x, int y)
	{
		this.plane = plane;
		this.x = x;
		this.y = y;
	}

	private static final class Sighting
	{
		private final TileObject object;
		private final List<ObjectRef> refs;

		private Sighting(TileObject object, List<ObjectRef> refs)
		{
			this.object = object;
			this.refs = refs;
		}
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

	public int getRotation()
	{
		return rotation;
	}

	void setRotation(int rotation)
	{
		this.rotation = rotation;
	}

	void add(TileObject object, List<ObjectRef> refs)
	{
		sightings.put(object.getHash(), new Sighting(object, refs));
		dirty = true;
	}

	void remove(TileObject object)
	{
		if (sightings.remove(object.getHash()) != null)
		{
			dirty = true;
		}
	}

	boolean isEmpty()
	{
		return sightings.isEmpty();
	}

	/**
	 * @return which room this chunk is, decided by majority vote over the objects standing in it,
	 * or {@code null} if nothing recognisable is here
	 */
	@Nullable
	public RoomDef getRoom()
	{
		if (dirty)
		{
			resolvedRoom = vote();
			dirty = false;
		}
		return resolvedRoom;
	}

	@Nullable
	private RoomDef vote()
	{
		// An object that can only mean one thing is worth more than one shared between rooms.
		Map<RoomDef, Integer> scores = new LinkedHashMap<>();
		for (Sighting sighting : sightings.values())
		{
			int weight = sighting.refs.size() == 1 ? 4 : 1;
			for (ObjectRef ref : sighting.refs)
			{
				scores.merge(ref.getRoom(), weight, Integer::sum);
			}
		}

		RoomDef best = null;
		int bestScore = 0;
		for (Map.Entry<RoomDef, Integer> entry : scores.entrySet())
		{
			if (entry.getValue() > bestScore)
			{
				best = entry.getKey();
				bestScore = entry.getValue();
			}
		}
		return best;
	}

	/**
	 * @return hotspot id to the furniture built there. Hotspots the player has left empty are not
	 * in this map; see {@link #getEmptyHotspots()}.
	 */
	public Map<String, FurnitureDef> getBuiltFurniture()
	{
		RoomDef room = getRoom();
		Map<String, FurnitureDef> built = new LinkedHashMap<>();
		if (room == null)
		{
			return built;
		}
		for (Sighting sighting : sightings.values())
		{
			for (ObjectRef ref : sighting.refs)
			{
				if (ref.getRoom() == room && ref.getFurniture() != null)
				{
					built.put(ref.getHotspot().getId(), ref.getFurniture());
				}
			}
		}
		return built;
	}

	/**
	 * @return hotspot id to the empty hotspot objects sitting there. Only populated while the player
	 * is in building mode, because that is when the game renders hotspots.
	 */
	public Map<String, List<TileObject>> getEmptyHotspots()
	{
		RoomDef room = getRoom();
		Map<String, List<TileObject>> empty = new LinkedHashMap<>();
		if (room == null)
		{
			return empty;
		}
		for (Sighting sighting : sightings.values())
		{
			for (ObjectRef ref : sighting.refs)
			{
				if (ref.getRoom() == room && ref.isEmptyHotspot())
				{
					empty.computeIfAbsent(ref.getHotspot().getId(), k -> new ArrayList<>())
						.add(sighting.object);
				}
			}
		}
		return empty;
	}

	/**
	 * @return the hotspot the given object belongs to, or {@code null}
	 */
	@Nullable
	public HotspotDef getHotspotFor(TileObject object)
	{
		RoomDef room = getRoom();
		Sighting sighting = sightings.get(object.getHash());
		if (room == null || sighting == null)
		{
			return null;
		}
		for (ObjectRef ref : sighting.refs)
		{
			if (ref.getRoom() == room)
			{
				return ref.getHotspot();
			}
		}
		return null;
	}
}
