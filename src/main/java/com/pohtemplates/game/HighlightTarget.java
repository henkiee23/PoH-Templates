/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.game;

import java.awt.Color;
import net.runelite.api.TileObject;

/**
 * A hotspot in the loaded scene the overlay should draw attention to, worked out once a tick rather
 * than every frame.
 */
public class HighlightTarget
{
	private final TileObject object;
	private final String label;
	private final Color colour;

	public HighlightTarget(TileObject object, String label, Color colour)
	{
		this.object = object;
		this.label = label;
		this.colour = colour;
	}

	public TileObject getObject()
	{
		return object;
	}

	public String getLabel()
	{
		return label;
	}

	public Color getColour()
	{
		return colour;
	}
}
