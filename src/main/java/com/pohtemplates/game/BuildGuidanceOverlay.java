/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.game;

import com.pohtemplates.PohTemplatesConfig;
import com.pohtemplates.PohTemplatesPlugin;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.util.List;
import javax.inject.Inject;
import net.runelite.api.Client;
import net.runelite.api.Perspective;
import net.runelite.api.Player;
import net.runelite.api.Point;
import net.runelite.api.TileObject;
import net.runelite.api.coords.LocalPoint;
import net.runelite.client.ui.overlay.Overlay;
import net.runelite.client.ui.overlay.OverlayLayer;
import net.runelite.client.ui.overlay.OverlayPosition;
import net.runelite.client.ui.overlay.OverlayUtil;
import net.runelite.client.ui.overlay.outline.ModelOutlineRenderer;

/**
 * Draws an outline round the hotspots the active plan still wants something built in, and writes
 * what to build beside them.
 * <p>
 * Purely visual: nothing here changes menu entries or sends anything to the game.
 */
public class BuildGuidanceOverlay extends Overlay
{
	private static final int OUTLINE_WIDTH = 2;
	private static final int OUTLINE_FEATHER = 4;
	private static final int LABEL_HEIGHT_OFFSET = 40;

	private final Client client;
	private final PohTemplatesPlugin plugin;
	private final PohTemplatesConfig config;
	private final ModelOutlineRenderer outlineRenderer;

	@Inject
	private BuildGuidanceOverlay(Client client, PohTemplatesPlugin plugin, PohTemplatesConfig config,
		ModelOutlineRenderer outlineRenderer)
	{
		this.client = client;
		this.plugin = plugin;
		this.config = config;
		this.outlineRenderer = outlineRenderer;
		setPosition(OverlayPosition.DYNAMIC);
		setLayer(OverlayLayer.ABOVE_SCENE);
	}

	@Override
	public Dimension render(Graphics2D graphics)
	{
		if (!config.showGuidance())
		{
			return null;
		}

		List<HighlightTarget> targets = plugin.getHighlightTargets();
		if (targets.isEmpty())
		{
			return null;
		}

		Player local = client.getLocalPlayer();
		if (local == null)
		{
			return null;
		}

		LocalPoint playerLocation = local.getLocalLocation();
		int maxDistance = config.guidanceRange() * Perspective.LOCAL_TILE_SIZE;
		boolean labels = config.showLabels();

		for (HighlightTarget target : targets)
		{
			TileObject object = target.getObject();
			LocalPoint location = object.getLocalLocation();
			if (location == null || playerLocation.distanceTo(location) > maxDistance)
			{
				continue;
			}

			Color colour = target.getColour();
			outlineRenderer.drawOutline(object, OUTLINE_WIDTH, colour, OUTLINE_FEATHER);

			if (labels && target.getLabel() != null)
			{
				Point textLocation = object.getCanvasLocation(LABEL_HEIGHT_OFFSET);
				if (textLocation != null)
				{
					OverlayUtil.renderTextLocation(graphics, textLocation, target.getLabel(), colour);
				}
			}
		}

		return null;
	}
}
