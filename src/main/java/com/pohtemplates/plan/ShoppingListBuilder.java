/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.plan;

import com.pohtemplates.PohTemplatesConfig;
import com.pohtemplates.data.ItemInfo;
import com.pohtemplates.data.Material;
import com.pohtemplates.data.PohData;
import com.pohtemplates.data.PohDataService;
import com.pohtemplates.game.BuildStep;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.inject.Inject;
import javax.inject.Singleton;
import net.runelite.api.gameval.ItemID;
import net.runelite.client.game.ItemManager;

/**
 * Rolls the outstanding build steps up into a materials list.
 * <p>
 * Prices come from RuneLite's own item price cache, so nothing here talks to the network.
 * {@link #build} touches {@link ItemManager}, so call it from the client thread.
 */
@Singleton
public class ShoppingListBuilder
{
	/** Nails are consumed even when they bend, so the list adds a margin for them. */
	private static final Set<Integer> NAIL_ITEM_IDS = new HashSet<>(Arrays.asList(
		ItemID.NAILS,
		ItemID.NAILS_BRONZE,
		ItemID.NAILS_IRON,
		ItemID.NAILS_BLACK,
		ItemID.NAILS_MITHRIL,
		ItemID.NAILS_ADAMANT,
		ItemID.NAILS_RUNE,
		ItemID.NAILS_DRAGON));

	private final PohDataService dataService;
	private final ItemManager itemManager;
	private final PohTemplatesConfig config;

	@Inject
	public ShoppingListBuilder(PohDataService dataService, ItemManager itemManager, PohTemplatesConfig config)
	{
		this.dataService = dataService;
		this.itemManager = itemManager;
		this.config = config;
	}

	public ShoppingList build(PlanProgress progress)
	{
		PohData data = dataService.get();

		Map<Integer, Integer> quantities = new LinkedHashMap<>();
		long coinCost = 0;
		int highestLevel = 0;

		for (BuildStep step : progress.getSteps())
		{
			coinCost += step.getCoinCost();
			highestLevel = Math.max(highestLevel, step.getLevelRequired());

			for (Material material : step.getMaterials())
			{
				quantities.merge(material.getItemId(), material.getQuantity(), Integer::sum);
			}
		}

		int nailBuffer = Math.max(0, Math.min(100, config.nailBuffer()));

		List<ShoppingListEntry> entries = new ArrayList<>(quantities.size());
		for (Map.Entry<Integer, Integer> entry : quantities.entrySet())
		{
			int itemId = entry.getKey();
			int quantity = entry.getValue();
			if (nailBuffer > 0 && NAIL_ITEM_IDS.contains(itemId))
			{
				quantity = (int) Math.ceil(quantity * (100 + nailBuffer) / 100d);
			}
			ItemInfo info = data.getItem(itemId);

			boolean tradeable = info == null || info.isTradeable();
			String name = info != null && info.getName() != null
				? info.getName()
				: "Item " + itemId;
			int unitPrice = tradeable ? Math.max(0, itemManager.getItemPrice(itemId)) : 0;

			entries.add(new ShoppingListEntry(itemId, name, quantity, unitPrice, tradeable,
				info == null ? null : new ArrayList<>(info.getSources())));
		}

		// Dearest first: that is the part of the list worth planning around.
		entries.sort((a, b) ->
		{
			int cmp = Long.compare(b.getTotalPrice(), a.getTotalPrice());
			return cmp != 0 ? cmp : a.getName().compareToIgnoreCase(b.getName());
		});

		return new ShoppingList(entries, coinCost, highestLevel);
	}
}
