/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.plan;

import com.pohtemplates.game.BuildStep;
import java.util.Collections;
import java.util.List;

/**
 * The difference between a plan and the house as it stands.
 */
public class PlanProgress
{
	private final List<BuildStep> steps;
	private final int plannedRooms;
	private final int matchingRooms;
	private final int plannedFurniture;
	private final int matchingFurniture;
	private final boolean houseSeen;

	PlanProgress(List<BuildStep> steps, int plannedRooms, int matchingRooms,
		int plannedFurniture, int matchingFurniture, boolean houseSeen)
	{
		this.steps = Collections.unmodifiableList(steps);
		this.plannedRooms = plannedRooms;
		this.matchingRooms = matchingRooms;
		this.plannedFurniture = plannedFurniture;
		this.matchingFurniture = matchingFurniture;
		this.houseSeen = houseSeen;
	}

	public List<BuildStep> getSteps()
	{
		return steps;
	}

	public int getPlannedRooms()
	{
		return plannedRooms;
	}

	public int getMatchingRooms()
	{
		return matchingRooms;
	}

	public int getPlannedFurniture()
	{
		return plannedFurniture;
	}

	public int getMatchingFurniture()
	{
		return matchingFurniture;
	}

	/**
	 * @return false when the plugin has not seen the player's house this session, in which case
	 * every step is listed as outstanding
	 */
	public boolean isHouseSeen()
	{
		return houseSeen;
	}

	public boolean isComplete()
	{
		return steps.isEmpty();
	}

	/**
	 * @return how far along the plan is, 0 - 1
	 */
	public double getFraction()
	{
		int total = plannedRooms + plannedFurniture;
		if (total == 0)
		{
			return 1d;
		}
		return (matchingRooms + matchingFurniture) / (double) total;
	}
}
