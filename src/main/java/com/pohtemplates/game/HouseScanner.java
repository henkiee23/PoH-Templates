/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.game;

import com.pohtemplates.data.ObjectRef;
import com.pohtemplates.data.PohData;
import com.pohtemplates.data.PohDataService;
import com.pohtemplates.data.RoomDef;
import com.pohtemplates.model.HouseFloor;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;
import javax.inject.Inject;
import javax.inject.Singleton;
import net.runelite.api.Client;
import net.runelite.api.Constants;
import net.runelite.api.Point;
import net.runelite.api.Tile;
import net.runelite.api.TileObject;
import net.runelite.api.WorldView;
import net.runelite.api.gameval.VarbitID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Keeps a live picture of the house the player is standing in.
 * <p>
 * The scene is never swept wholesale; objects are added and removed as the client reports them, and
 * the picture is thrown away when a new scene loads. Every 8x8 chunk of the scene is one room square,
 * so the chunk index doubles as the house grid coordinate.
 */
@Singleton
public class HouseScanner
{
	private static final Logger log = LoggerFactory.getLogger(HouseScanner.class);

	/** A house grid is 13x13 rooms, which is exactly the 104x104 scene divided into 8x8 chunks. */
	private static final int GRID = HouseTemplate.GRID_SIZE;

	private final Client client;
	private final PohDataService dataService;

	private final Map<Integer, DetectedRoom> rooms = new HashMap<>();
	private final Map<Long, Integer> objectCells = new HashMap<>();

	/**
	 * Which floor each plane of the loaded scene is. Worked out from the rooms actually standing
	 * there rather than assumed, because the plane a floor occupies is not fixed: the house scene
	 * puts the ground floor at plane 0, and the dungeon is its own scene that also starts at 0.
	 */
	private final Map<Integer, Integer> floorByScenePlane = new HashMap<>();
	private boolean floorsStale = true;

	@Inject
	public HouseScanner(Client client, PohDataService dataService)
	{
		this.client = client;
		this.dataService = dataService;
	}

	/**
	 * @return true if anything recognisable as a house has been seen in the current scene
	 */
	public boolean isInHouse()
	{
		return !rooms.isEmpty();
	}

	/**
	 * @return true while the player has the house in building mode, which is when the game draws
	 * the empty build hotspots
	 */
	public boolean isBuildingMode()
	{
		return client.getVarbitValue(VarbitID.POH_BUILDING_MODE) == 1;
	}

	public Collection<DetectedRoom> getRooms()
	{
		return rooms.values();
	}

	/**
	 * @param floor a floor as a plan records it, i.e. {@link HouseFloor#getPlane()}, not a plane of
	 *              the loaded scene
	 */
	@Nullable
	public DetectedRoom getRoom(int floor, int x, int y)
	{
		Integer scenePlane = scenePlaneFor(floor);
		return scenePlane == null ? null : rooms.get(key(scenePlane, x, y));
	}

	/**
	 * @return the plane of the loaded scene holding the given floor, or {@code null} if that floor
	 * is not part of the scene the player is standing in
	 */
	@Nullable
	private Integer scenePlaneFor(int floor)
	{
		resolveFloors();
		for (Map.Entry<Integer, Integer> entry : floorByScenePlane.entrySet())
		{
			if (entry.getValue() == floor)
			{
				return entry.getKey();
			}
		}
		return null;
	}

	/**
	 * @return the floor the given scene plane holds, as a plan records it
	 */
	private int floorFor(int scenePlane)
	{
		resolveFloors();
		Integer floor = floorByScenePlane.get(scenePlane);
		return floor == null ? scenePlane : floor;
	}

	/**
	 * Works out which floor each plane of the loaded scene is.
	 * <p>
	 * The plane a floor sits on is not fixed, so it is deduced from what is standing there: a
	 * garden can only be outdoors and so marks the ground floor, and an oubliette or dungeon room
	 * can only be in the basement. Anything left over is placed relative to whichever of those was
	 * found. If nothing identifiable is loaded, the lowest plane present is taken as the ground
	 * floor, which is what the house scene does.
	 */
	private void resolveFloors()
	{
		if (!floorsStale)
		{
			return;
		}
		floorsStale = false;
		floorByScenePlane.clear();

		Integer groundPlane = null;
		Integer dungeonPlane = null;
		java.util.TreeSet<Integer> planes = new java.util.TreeSet<>();

		for (DetectedRoom room : rooms.values())
		{
			planes.add(room.getPlane());

			RoomDef def = room.getRoom();
			if (def == null)
			{
				continue;
			}
			if (isOnlyOn(def, HouseFloor.DUNGEON.getPlane()))
			{
				dungeonPlane = room.getPlane();
			}
			else if (isOnlyOn(def, HouseFloor.GROUND.getPlane()))
			{
				groundPlane = room.getPlane();
			}
		}

		if (groundPlane == null && dungeonPlane == null && !planes.isEmpty())
		{
			// Nothing gave the game away, so assume the lowest loaded plane is the ground floor.
			groundPlane = planes.first();
		}

		for (Integer plane : planes)
		{
			if (dungeonPlane != null && plane.equals(dungeonPlane))
			{
				floorByScenePlane.put(plane, HouseFloor.DUNGEON.getPlane());
			}
			else if (groundPlane != null)
			{
				int delta = plane - groundPlane;
				floorByScenePlane.put(plane, delta <= 0
					? (delta == 0 ? HouseFloor.GROUND.getPlane() : HouseFloor.DUNGEON.getPlane())
					: HouseFloor.UPPER.getPlane());
			}
			else
			{
				// Only the dungeon is loaded; anything above it is the ground floor.
				floorByScenePlane.put(plane, plane.equals(dungeonPlane)
					? HouseFloor.DUNGEON.getPlane()
					: HouseFloor.GROUND.getPlane());
			}
		}

		log.debug("POH floors resolved: {}", floorByScenePlane);
	}

	private static boolean isOnlyOn(RoomDef def, int floor)
	{
		return def.getPlanes().size() == 1 && def.getPlanes().get(0) == floor;
	}

	public void clear()
	{
		rooms.clear();
		objectCells.clear();
		floorByScenePlane.clear();
		floorsStale = true;
	}

	public void onObjectSpawned(Tile tile, TileObject object)
	{
		PohData data = dataService.get();
		List<ObjectRef> refs = data.getObjectRefs(object.getId());
		if (refs.isEmpty())
		{
			return;
		}

		Point scene = tile.getSceneLocation();
		int gridX = scene.getX() / Constants.CHUNK_SIZE;
		int gridY = scene.getY() / Constants.CHUNK_SIZE;
		if (gridX < 0 || gridX >= GRID || gridY < 0 || gridY >= GRID)
		{
			return;
		}

		int plane = tile.getPlane();
		int cell = key(plane, gridX, gridY);
		DetectedRoom room = rooms.computeIfAbsent(cell, k -> new DetectedRoom(plane, gridX, gridY));
		room.setRotation(readRotation(plane, gridX, gridY));
		room.add(object, refs);
		objectCells.put(object.getHash(), cell);
		floorsStale = true;
	}

	public void onObjectDespawned(TileObject object)
	{
		Integer cell = objectCells.remove(object.getHash());
		if (cell == null)
		{
			return;
		}
		DetectedRoom room = rooms.get(cell);
		if (room == null)
		{
			return;
		}
		room.remove(object);
		if (room.isEmpty())
		{
			rooms.remove(cell);
		}
		floorsStale = true;
	}

	/**
	 * Reads how the game turned this chunk when it built the instance. The bit layout is documented
	 * on {@code WorldView#getInstanceTemplateChunks()}.
	 */
	private int readRotation(int plane, int gridX, int gridY)
	{
		WorldView worldView = client.getTopLevelWorldView();
		if (worldView == null || !worldView.isInstance())
		{
			return 0;
		}

		int[][][] chunks = worldView.getInstanceTemplateChunks();
		if (chunks == null
			|| plane < 0 || plane >= chunks.length
			|| gridX < 0 || gridX >= chunks[plane].length
			|| gridY < 0 || gridY >= chunks[plane][gridX].length)
		{
			return 0;
		}

		int chunkData = chunks[plane][gridX][gridY];
		if (chunkData == -1)
		{
			return 0;
		}
		return chunkData >> 1 & 0x3;
	}

	/**
	 * Turns what is currently loaded into a plan the user can edit and share.
	 */
	public HouseTemplate toTemplate(String name)
	{
		HouseTemplate template = new HouseTemplate(name);
		for (DetectedRoom detected : rooms.values())
		{
			if (detected.getRoom() == null)
			{
				continue;
			}

			PlannedRoom planned = new PlannedRoom(
				floorFor(detected.getPlane()),
				detected.getX(),
				detected.getY(),
				detected.getRoom().getId(),
				detected.getRotation());

			detected.getBuiltFurniture()
				.forEach((hotspotId, furniture) -> planned.getFurniture().put(hotspotId, furniture.getId()));

			template.putRoom(planned);
		}
		return template;
	}

	/**
	 * @return the detected rooms sorted for stable display, south-west first
	 */
	public List<DetectedRoom> getRoomsSorted()
	{
		List<DetectedRoom> sorted = new ArrayList<>(rooms.values());
		sorted.sort((a, b) ->
		{
			int cmp = Integer.compare(a.getPlane(), b.getPlane());
			if (cmp != 0)
			{
				return cmp;
			}
			cmp = Integer.compare(a.getY(), b.getY());
			return cmp != 0 ? cmp : Integer.compare(a.getX(), b.getX());
		});
		return sorted;
	}

	private static int key(int plane, int x, int y)
	{
		return (plane << 16) | (x << 8) | y;
	}
}
