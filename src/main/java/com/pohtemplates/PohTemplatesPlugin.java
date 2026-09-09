/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates;

import com.google.inject.Provides;
import com.pohtemplates.data.FurnitureDef;
import com.pohtemplates.data.PohDataService;
import com.pohtemplates.game.BuildGuidanceOverlay;
import com.pohtemplates.game.BuildStep;
import com.pohtemplates.game.DetectedRoom;
import com.pohtemplates.game.HighlightTarget;
import com.pohtemplates.game.HouseScanner;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import com.pohtemplates.plan.PlanComparator;
import com.pohtemplates.plan.PlanProgress;
import com.pohtemplates.plan.ShoppingList;
import com.pohtemplates.plan.ShoppingListBuilder;
import com.pohtemplates.store.TemplateStore;
import com.pohtemplates.ui.PohTemplatesPanel;
import java.awt.Color;
import java.awt.Point;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.Nullable;
import javax.inject.Inject;
import javax.swing.SwingUtilities;
import net.runelite.api.Client;
import net.runelite.api.GameState;
import net.runelite.api.Skill;
import net.runelite.api.TileObject;
import net.runelite.api.events.DecorativeObjectDespawned;
import net.runelite.api.events.DecorativeObjectSpawned;
import net.runelite.api.events.GameObjectDespawned;
import net.runelite.api.events.GameObjectSpawned;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.GameTick;
import net.runelite.api.events.GroundObjectDespawned;
import net.runelite.api.events.GroundObjectSpawned;
import net.runelite.api.events.WallObjectDespawned;
import net.runelite.api.events.WallObjectSpawned;
import net.runelite.client.callback.ClientThread;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.ui.ClientToolbar;
import net.runelite.client.ui.NavigationButton;
import net.runelite.client.ui.overlay.OverlayManager;
import net.runelite.client.util.ImageUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@PluginDescriptor(
	name = "POH Templates",
	description = "Plan your house layout, get a materials shopping list, and be shown what to build where",
	tags = {"construction", "poh", "house", "planner", "template", "ironman", "build"}
)
public class PohTemplatesPlugin extends Plugin
{
	private static final Logger log = LoggerFactory.getLogger(PohTemplatesPlugin.class);

	@Inject
	private Client client;

	@Inject
	private ClientThread clientThread;

	@Inject
	private ClientToolbar clientToolbar;

	@Inject
	private OverlayManager overlayManager;

	@Inject
	private BuildGuidanceOverlay overlay;

	@Inject
	private PohTemplatesConfig config;

	@Inject
	private PohDataService dataService;

	@Inject
	private TemplateStore templateStore;

	@Inject
	private PlanComparator planComparator;

	@Inject
	private ShoppingListBuilder shoppingListBuilder;

	@Inject
	private HouseScanner houseScanner;

	@Inject
	private PohTemplatesPanel panel;

	private NavigationButton navButton;

	/** Read by the overlay on the client thread and replaced wholesale, never mutated in place. */
	private volatile List<HighlightTarget> highlightTargets = Collections.emptyList();
	private volatile PlanProgress progress;

	private HouseTemplate activeTemplate;
	private Point alignment = new Point(0, 0);
	private boolean sceneDirty = true;

	@Provides
	PohTemplatesConfig provideConfig(ConfigManager configManager)
	{
		return configManager.getConfig(PohTemplatesConfig.class);
	}

	@Override
	protected void startUp()
	{
		overlayManager.add(overlay);

		panel.init(this);

		final BufferedImage icon = ImageUtil.loadImageResource(PohTemplatesPlugin.class, "/com/pohtemplates/icon.png");
		navButton = NavigationButton.builder()
			.tooltip("POH Templates")
			.icon(icon)
			.priority(6)
			.panel(panel)
			.build();
		clientToolbar.addNavigation(navButton);

		String activeId = config.activeTemplate();
		if (activeId != null && !activeId.isEmpty())
		{
			activeTemplate = templateStore.get(activeId);
		}

		SwingUtilities.invokeLater(panel::rebuild);
		log.debug("POH Templates started");
	}

	@Override
	protected void shutDown()
	{
		overlayManager.remove(overlay);
		clientToolbar.removeNavigation(navButton);
		navButton = null;
		houseScanner.clear();
		highlightTargets = Collections.emptyList();
		progress = null;
		log.debug("POH Templates stopped");
	}

	// -------------------------------------------------------------------------------------------
	// Scene tracking
	// -------------------------------------------------------------------------------------------

	@Subscribe
	public void onGameStateChanged(GameStateChanged event)
	{
		GameState state = event.getGameState();
		if (state == GameState.LOADING || state == GameState.HOPPING || state == GameState.LOGIN_SCREEN)
		{
			houseScanner.clear();
			highlightTargets = Collections.emptyList();
			sceneDirty = true;
		}
	}

	@Subscribe
	public void onGameObjectSpawned(GameObjectSpawned event)
	{
		houseScanner.onObjectSpawned(event.getTile(), event.getGameObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onGameObjectDespawned(GameObjectDespawned event)
	{
		houseScanner.onObjectDespawned(event.getGameObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onWallObjectSpawned(WallObjectSpawned event)
	{
		houseScanner.onObjectSpawned(event.getTile(), event.getWallObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onWallObjectDespawned(WallObjectDespawned event)
	{
		houseScanner.onObjectDespawned(event.getWallObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onDecorativeObjectSpawned(DecorativeObjectSpawned event)
	{
		houseScanner.onObjectSpawned(event.getTile(), event.getDecorativeObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onDecorativeObjectDespawned(DecorativeObjectDespawned event)
	{
		houseScanner.onObjectDespawned(event.getDecorativeObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onGroundObjectSpawned(GroundObjectSpawned event)
	{
		houseScanner.onObjectSpawned(event.getTile(), event.getGroundObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onGroundObjectDespawned(GroundObjectDespawned event)
	{
		houseScanner.onObjectDespawned(event.getGroundObject());
		sceneDirty = true;
	}

	@Subscribe
	public void onGameTick(GameTick tick)
	{
		if (!sceneDirty)
		{
			return;
		}
		sceneDirty = false;
		recompute();
	}

	// -------------------------------------------------------------------------------------------
	// Plan state, called from both the client thread and the Swing thread
	// -------------------------------------------------------------------------------------------

	@Nullable
	public HouseTemplate getActiveTemplate()
	{
		return activeTemplate;
	}

	public void setActiveTemplate(@Nullable HouseTemplate template)
	{
		this.activeTemplate = template;
		config.setActiveTemplate(template == null ? "" : template.getId());
		this.alignment = new Point(0, 0);
		clientThread.invokeLater(this::recompute);
	}

	/**
	 * Saves the active plan and refreshes everything that depends on it.
	 */
	public void planChanged()
	{
		if (activeTemplate != null)
		{
			templateStore.put(activeTemplate);
		}
		clientThread.invokeLater(this::recompute);
	}

	public Point getAlignment()
	{
		return new Point(alignment);
	}

	public void setAlignment(Point alignment)
	{
		this.alignment = alignment == null ? new Point(0, 0) : new Point(alignment);
		clientThread.invokeLater(this::recompute);
	}

	/**
	 * Lines the active plan up with the house the player is standing in.
	 */
	public void autoAlign()
	{
		clientThread.invokeLater(() ->
		{
			if (activeTemplate != null)
			{
				alignment = planComparator.suggestAlignment(activeTemplate, houseScanner);
			}
			recompute();
		});
	}

	@Nullable
	public PlanProgress getProgress()
	{
		return progress;
	}

	/**
	 * @return the rooms in the active plan that share no door with a neighbour. Pure plan maths, so
	 * this is safe to call from the Swing thread.
	 */
	public Set<PlannedRoom> getUnreachableRooms()
	{
		HouseTemplate template = activeTemplate;
		return template == null
			? Collections.emptySet()
			: planComparator.findUnreachableRooms(template);
	}

	public List<HighlightTarget> getHighlightTargets()
	{
		return highlightTargets;
	}

	public HouseScanner getHouseScanner()
	{
		return houseScanner;
	}

	public TemplateStore getTemplateStore()
	{
		return templateStore;
	}

	public PohDataService getDataService()
	{
		return dataService;
	}

	public PohTemplatesConfig getConfig()
	{
		return config;
	}

	/**
	 * Captures the loaded house as a new plan. Must run on the client thread.
	 */
	public HouseTemplate captureCurrentHouse(String name)
	{
		return houseScanner.toTemplate(name);
	}

	public void runOnClientThread(Runnable runnable)
	{
		clientThread.invokeLater(runnable);
	}

	/**
	 * Recomputes the plan comparison, the shopping list and the overlay targets. Client thread only,
	 * because it reads the scene and the item price cache.
	 */
	public void recompute()
	{
		HouseTemplate template = activeTemplate;
		if (template == null)
		{
			progress = null;
			highlightTargets = Collections.emptyList();
			pushToPanel(null, null);
			return;
		}

		PlanProgress computed = planComparator.compare(template, houseScanner, alignment);
		progress = computed;
		highlightTargets = buildHighlightTargets(computed);

		ShoppingList shoppingList = shoppingListBuilder.build(computed);
		pushToPanel(computed, shoppingList);
	}

	private void pushToPanel(@Nullable PlanProgress computed, @Nullable ShoppingList shoppingList)
	{
		SwingUtilities.invokeLater(() -> panel.onProgressUpdated(computed, shoppingList));
	}

	/**
	 * Matches outstanding furniture steps to the empty hotspot objects sitting in the loaded scene.
	 * Hotspots are only rendered by the game while the house is in building mode, so outside it
	 * there is nothing to outline.
	 */
	private List<HighlightTarget> buildHighlightTargets(PlanProgress computed)
	{
		if (!config.showGuidance() || !houseScanner.isInHouse() || !houseScanner.isBuildingMode())
		{
			return Collections.emptyList();
		}

		int level = client.getBoostedSkillLevel(Skill.CONSTRUCTION);
		boolean hideUnaffordable = config.hideWhenUnaffordable();
		Color plannedColour = config.plannedColour();
		Color mismatchColour = config.mismatchColour();

		List<HighlightTarget> targets = new ArrayList<>();
		for (BuildStep step : computed.getSteps())
		{
			if (step.getType() != BuildStep.Type.BUILD_FURNITURE || step.getHotspot() == null)
			{
				continue;
			}
			if (hideUnaffordable && step.getLevelRequired() > level)
			{
				continue;
			}

			DetectedRoom room = houseScanner.getRoom(step.getPlane(), step.getX(), step.getY());
			if (room == null)
			{
				continue;
			}

			Map<String, List<TileObject>> empty = room.getEmptyHotspots();
			List<TileObject> objects = empty.get(step.getHotspot().getId());
			if (objects == null || objects.isEmpty())
			{
				continue;
			}

			FurnitureDef furniture = step.getFurniture();
			String label = furniture == null ? step.describe() : furniture.getName();
			Color colour = step.getExisting() == null ? plannedColour : mismatchColour;

			for (TileObject object : objects)
			{
				targets.add(new HighlightTarget(object, label, colour));
			}
		}

		return Collections.unmodifiableList(targets);
	}
}
