/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates;

import java.awt.Color;
import net.runelite.client.config.Alpha;
import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;
import net.runelite.client.config.ConfigSection;
import net.runelite.client.config.Range;
import net.runelite.client.config.Units;

@ConfigGroup(PohTemplatesConfig.GROUP)
public interface PohTemplatesConfig extends Config
{
	String GROUP = "poh-templates";

	@ConfigSection(
		name = "In-game guidance",
		description = "How the plugin points out what to build",
		position = 0
	)
	String guidanceSection = "guidance";

	@ConfigSection(
		name = "Shopping list",
		description = "How materials are totalled up",
		position = 1
	)
	String shoppingSection = "shopping";

	@ConfigItem(
		keyName = "showGuidance",
		name = "Highlight build hotspots",
		description = "Outline the hotspots your plan still wants something built in, while you are in building mode",
		section = guidanceSection,
		position = 0
	)
	default boolean showGuidance()
	{
		return true;
	}

	@ConfigItem(
		keyName = "showLabels",
		name = "Show labels",
		description = "Write what to build next to each highlighted hotspot",
		section = guidanceSection,
		position = 1
	)
	default boolean showLabels()
	{
		return true;
	}

	@Alpha
	@ConfigItem(
		keyName = "plannedColour",
		name = "To build",
		description = "Colour for a hotspot your plan wants something in",
		section = guidanceSection,
		position = 2
	)
	default Color plannedColour()
	{
		return new Color(0x2E, 0xCC, 0x71, 0xC0);
	}

	@Alpha
	@ConfigItem(
		keyName = "mismatchColour",
		name = "Wrong item built",
		description = "Colour for a hotspot that already holds something other than what the plan asks for",
		section = guidanceSection,
		position = 3
	)
	default Color mismatchColour()
	{
		return new Color(0xE6, 0x7E, 0x22, 0xC0);
	}

	@ConfigItem(
		keyName = "hideWhenUnaffordable",
		name = "Only show what I can build",
		description = "Hide hotspots whose furniture needs a higher Construction level than you have",
		section = guidanceSection,
		position = 4
	)
	default boolean hideWhenUnaffordable()
	{
		return false;
	}

	@Range(min = 1, max = 30)
	@Units(Units.TILES)
	@ConfigItem(
		keyName = "guidanceRange",
		name = "Highlight range",
		description = "How far away a hotspot can be and still be highlighted",
		section = guidanceSection,
		position = 5
	)
	default int guidanceRange()
	{
		return 12;
	}

	@Range(min = 0, max = 100)
	@Units(Units.PERCENT)
	@ConfigItem(
		keyName = "nailBuffer",
		name = "Spare nails",
		description = "Nails bend and are lost when building. This adds a margin to the nails on the shopping list",
		section = shoppingSection,
		position = 0
	)
	default int nailBuffer()
	{
		return 25;
	}

	@ConfigItem(
		keyName = "showIronmanSources",
		name = "Show ironman sources",
		description = "List where each material can be bought or made without the Grand Exchange",
		section = shoppingSection,
		position = 1
	)
	default boolean showIronmanSources()
	{
		return true;
	}

	@ConfigItem(
		keyName = "activeTemplate",
		name = "",
		description = "",
		hidden = true
	)
	default String activeTemplate()
	{
		return "";
	}

	@ConfigItem(
		keyName = "activeTemplate",
		name = "",
		description = "",
		hidden = true
	)
	void setActiveTemplate(String id);
}
