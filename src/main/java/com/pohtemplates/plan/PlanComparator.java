/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.plan;

import com.pohtemplates.data.FurnitureDef;
import com.pohtemplates.data.HotspotDef;
import com.pohtemplates.data.PohData;
import com.pohtemplates.data.PohDataService;
import com.pohtemplates.data.RoomDef;
import com.pohtemplates.game.BuildStep;
import com.pohtemplates.game.DetectedRoom;
import com.pohtemplates.game.HouseScanner;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.awt.Point;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.Nullable;
import javax.inject.Inject;
import javax.inject.Singleton;

/**
 * Works out what is left to build, by comparing a plan against the house the player is standing in.
 */
@Singleton
public class PlanComparator
{
	private final PohDataService dataService;

	@Inject
	public PlanComparator(PohDataService dataService)
	{
		this.dataService = dataService;
	}

	/**
	 * @param plan    the plan to work towards
	 * @param scanner the live house, or {@code null} when the player is not in their house
	 * @param offset  grid offset applied to the plan before comparing; see
	 *                {@link #suggestAlignment(HouseTemplate, HouseScanner)}
	 */
	public PlanProgress compare(HouseTemplate plan, @Nullable HouseScanner scanner, Point offset)
	{
		PohData data = dataService.get();
		List<BuildStep> steps = new ArrayList<>();

		boolean houseSeen = scanner != null && scanner.isInHouse();
		int dx = offset == null ? 0 : offset.x;
		int dy = offset == null ? 0 : offset.y;

		int plannedRooms = 0;
		int matchingRooms = 0;
		int plannedFurniture = 0;
		int matchingFurniture = 0;

		for (PlannedRoom planned : plan.getRooms())
		{
			RoomDef roomDef = data.getRoom(planned.getRoom());
			if (roomDef == null)
			{
				// The plan references a room this build of the plugin does not know about.
				continue;
			}

			plannedRooms++;

			int gx = planned.getX() + dx;
			int gy = planned.getY() + dy;
			DetectedRoom detected = houseSeen ? scanner.getRoom(planned.getPlane(), gx, gy) : null;
			RoomDef detectedDef = detected == null ? null : detected.getRoom();

			if (detectedDef == null)
			{
				steps.add(BuildStep.room(BuildStep.Type.ADD_ROOM,
					planned.getPlane(), gx, gy, roomDef, planned.getRotation()));
			}
			else if (detectedDef != roomDef)
			{
				steps.add(BuildStep.room(BuildStep.Type.REPLACE_ROOM,
					planned.getPlane(), gx, gy, roomDef, planned.getRotation()));
			}
			else
			{
				matchingRooms++;
				if (detected.getRotation() != planned.getRotation())
				{
					steps.add(BuildStep.room(BuildStep.Type.ROTATE_ROOM,
						planned.getPlane(), gx, gy, roomDef, planned.getRotation()));
				}
			}

			Map<String, FurnitureDef> built = detectedDef == roomDef && detected != null
				? detected.getBuiltFurniture()
				: java.util.Collections.emptyMap();

			for (Map.Entry<String, String> wanted : planned.getFurniture().entrySet())
			{
				HotspotDef hotspot = roomDef.getHotspot(wanted.getKey());
				if (hotspot == null)
				{
					continue;
				}
				FurnitureDef furniture = hotspot.getOption(wanted.getValue());
				if (furniture == null)
				{
					continue;
				}

				plannedFurniture++;

				FurnitureDef existing = built.get(hotspot.getId());
				if (existing != null && existing.getId().equals(furniture.getId()))
				{
					matchingFurniture++;
					continue;
				}

				steps.add(BuildStep.furniture(planned.getPlane(), gx, gy,
					roomDef, planned.getRotation(), hotspot, furniture, existing));
			}
		}

		steps.sort(PlanComparator::compareSteps);

		return new PlanProgress(steps, plannedRooms, matchingRooms,
			plannedFurniture, matchingFurniture, houseSeen);
	}

	/**
	 * Rooms before the furniture that goes in them, then by level so the list reads as an order the
	 * player can actually work through, then by position so it is stable.
	 */
	private static int compareSteps(BuildStep a, BuildStep b)
	{
		boolean aRoom = a.getType() != BuildStep.Type.BUILD_FURNITURE;
		boolean bRoom = b.getType() != BuildStep.Type.BUILD_FURNITURE;
		if (aRoom != bRoom)
		{
			return aRoom ? -1 : 1;
		}

		int cmp = Integer.compare(a.getLevelRequired(), b.getLevelRequired());
		if (cmp != 0)
		{
			return cmp;
		}
		cmp = Integer.compare(a.getPlane(), b.getPlane());
		if (cmp != 0)
		{
			return cmp;
		}
		cmp = Integer.compare(a.getY(), b.getY());
		if (cmp != 0)
		{
			return cmp;
		}
		return Integer.compare(a.getX(), b.getX());
	}

	/**
	 * Finds the grid offset that lines an imported plan up with the player's actual house.
	 * <p>
	 * Plans captured from a house already sit on the right squares, but one written by somebody else
	 * may be drawn anywhere on the grid. This slides the plan over the house and keeps the offset
	 * that puts the most rooms of the same type on top of each other.
	 *
	 * @return the offset to add to plan coordinates, or {@code (0, 0)} if nothing lines up
	 */
	public Point suggestAlignment(HouseTemplate plan, @Nullable HouseScanner scanner)
	{
		if (scanner == null || !scanner.isInHouse() || plan.getRooms().isEmpty())
		{
			return new Point(0, 0);
		}

		PohData data = dataService.get();
		int span = HouseTemplate.GRID_SIZE - 1;

		Point best = new Point(0, 0);
		int bestScore = -1;

		for (int dx = -span; dx <= span; dx++)
		{
			for (int dy = -span; dy <= span; dy++)
			{
				int score = 0;
				for (PlannedRoom planned : plan.getRooms())
				{
					RoomDef roomDef = data.getRoom(planned.getRoom());
					if (roomDef == null)
					{
						continue;
					}
					DetectedRoom detected = scanner.getRoom(planned.getPlane(),
						planned.getX() + dx, planned.getY() + dy);
					if (detected != null && detected.getRoom() == roomDef)
					{
						score++;
					}
				}
				if (score > bestScore)
				{
					bestScore = score;
					best = new Point(dx, dy);
				}
			}
		}

		return bestScore <= 0 ? new Point(0, 0) : best;
	}

	/**
	 * Flags rooms that share no door with any neighbour. The game will not let a house be built that
	 * way, so the editor shows these as a warning rather than refusing the placement.
	 *
	 * @return the offending rooms; a plan with a single room never flags anything
	 */
	public Set<PlannedRoom> findUnreachableRooms(HouseTemplate plan)
	{
		PohData data = dataService.get();
		Set<PlannedRoom> unreachable = new HashSet<>();

		if (plan.getRooms().size() < 2)
		{
			return unreachable;
		}

		for (PlannedRoom planned : plan.getRooms())
		{
			RoomDef roomDef = data.getRoom(planned.getRoom());
			if (roomDef == null || roomDef.getDoors().isEmpty())
			{
				continue;
			}

			boolean connected = false;
			for (com.pohtemplates.data.Direction door : roomDef.getDoors(planned.getRotation()))
			{
				PlannedRoom neighbour = plan.getRoomAt(planned.getPlane(),
					planned.getX() + door.getDx(), planned.getY() + door.getDy());
				if (neighbour == null)
				{
					continue;
				}
				RoomDef neighbourDef = data.getRoom(neighbour.getRoom());
				if (neighbourDef == null)
				{
					continue;
				}
				if (neighbourDef.getDoors(neighbour.getRotation()).contains(door.opposite()))
				{
					connected = true;
					break;
				}
			}

			if (!connected)
			{
				unreachable.add(planned);
			}
		}

		return unreachable;
	}
}
