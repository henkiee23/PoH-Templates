/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.PohTemplatesConfig;
import com.pohtemplates.PohTemplatesPlugin;
import com.pohtemplates.data.PohData;
import com.pohtemplates.data.PohDataService;
import com.pohtemplates.model.HouseFloor;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.plan.PlanProgress;
import com.pohtemplates.plan.ShoppingList;
import com.pohtemplates.share.ShareCodeException;
import com.pohtemplates.share.ShareCodec;
import com.pohtemplates.store.TemplateStore;
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.Toolkit;
import java.awt.datatransfer.StringSelection;
import java.util.List;
import javax.annotation.Nullable;
import javax.inject.Inject;
import javax.inject.Singleton;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.FontManager;
import net.runelite.client.ui.PluginPanel;
import net.runelite.client.ui.components.PluginErrorPanel;
import net.runelite.client.ui.components.materialtabs.MaterialTab;
import net.runelite.client.ui.components.materialtabs.MaterialTabGroup;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The plugin's side panel: pick a plan, lay out the house, then look at what is left to build and
 * what it will cost.
 */
@Singleton
public class PohTemplatesPanel extends PluginPanel
{
	private static final Logger log = LoggerFactory.getLogger(PohTemplatesPanel.class);

	private final PohDataService dataService;
	private final TemplateStore templateStore;
	private final ShareCodec shareCodec;
	private final PohTemplatesConfig config;

	private final JComboBox<ComboItem<HouseTemplate>> templateCombo = new JComboBox<>();
	private final JComboBox<HouseFloor> floorCombo = new JComboBox<>(HouseFloor.values());
	private final JPanel tabDisplay = new JPanel(new BorderLayout());
	private final PluginErrorPanel errorPanel = new PluginErrorPanel();

	private HouseGridPanel grid;
	private RoomEditorPanel roomEditor;
	private BuildStepsPanel buildSteps;
	private ShoppingPanel shopping;

	private PohTemplatesPlugin plugin;
	private boolean updatingCombo;

	@Inject
	PohTemplatesPanel(PohDataService dataService, TemplateStore templateStore,
		ShareCodec shareCodec, PohTemplatesConfig config)
	{
		this.dataService = dataService;
		this.templateStore = templateStore;
		this.shareCodec = shareCodec;
		this.config = config;
	}

	/**
	 * Builds the panel. Called once from the plugin's startUp, before the nav button is added.
	 */
	public void init(PohTemplatesPlugin plugin)
	{
		this.plugin = plugin;

		PohData data = dataService.get();

		setBackground(ColorScheme.DARK_GRAY_COLOR);

		if (data.isEmpty())
		{
			errorPanel.setContent("POH Templates",
				"The bundled house data could not be loaded, so this plugin cannot do anything. "
					+ "Please report this.");
			add(errorPanel);
			return;
		}

		add(buildHeader());

		grid = new HouseGridPanel(data, this::onCellSelected);
		roomEditor = new RoomEditorPanel(data, this::onPlanEdited);
		buildSteps = new BuildStepsPanel(data);
		shopping = new ShoppingPanel(config);

		MaterialTabGroup tabs = new MaterialTabGroup(tabDisplay);
		MaterialTab layoutTab = new MaterialTab("Layout", tabs, buildLayoutTab());
		MaterialTab buildTab = new MaterialTab("To build", tabs, buildSteps);
		MaterialTab shoppingTab = new MaterialTab("Shopping", tabs, shopping);
		tabs.addTab(layoutTab);
		tabs.addTab(buildTab);
		tabs.addTab(shoppingTab);
		tabs.select(layoutTab);

		add(tabs);
		add(tabDisplay);
	}

	private JPanel buildHeader()
	{
		JPanel header = new JPanel(new BorderLayout(0, 4));
		header.setBackground(ColorScheme.DARK_GRAY_COLOR);

		templateCombo.setFocusable(false);
		templateCombo.addActionListener(e -> onTemplateSelected());

		JPanel buttons = new JPanel(new GridLayout(3, 2, 3, 3));
		buttons.setBackground(ColorScheme.DARK_GRAY_COLOR);
		buttons.add(button("New", "Start an empty plan", e -> newPlan()));
		buttons.add(button("Capture", "Copy the house you are standing in into a new plan", e -> capture()));
		buttons.add(button("Import", "Paste a share code from somebody else", e -> importPlan()));
		buttons.add(button("Export", "Get a share code for this plan", e -> exportPlan()));
		buttons.add(button("Rename", "Rename this plan", e -> renamePlan()));
		buttons.add(button("Delete", "Delete this plan", e -> deletePlan()));

		header.add(templateCombo, BorderLayout.NORTH);
		header.add(buttons, BorderLayout.CENTER);
		return header;
	}

	private JPanel buildLayoutTab()
	{
		JPanel layout = new JPanel();
		layout.setLayout(new BorderLayout(0, 4));
		layout.setBackground(ColorScheme.DARK_GRAY_COLOR);

		floorCombo.setFocusable(false);
		floorCombo.setSelectedItem(HouseFloor.GROUND);
		floorCombo.addActionListener(e ->
		{
			HouseFloor floor = (HouseFloor) floorCombo.getSelectedItem();
			if (floor != null)
			{
				grid.setPlane(floor.getPlane());
				roomEditor.clear();
			}
		});

		JPanel top = new JPanel(new BorderLayout(0, 4));
		top.setBackground(ColorScheme.DARK_GRAY_COLOR);
		top.add(floorCombo, BorderLayout.NORTH);

		JPanel gridHolder = new JPanel();
		gridHolder.setBackground(ColorScheme.DARK_GRAY_COLOR);
		gridHolder.add(grid);
		top.add(gridHolder, BorderLayout.CENTER);

		JLabel hint = new JLabel("<html><body style='width:195px'>"
			+ "Click a square to place a room. North is up.<br>"
			+ "Doors: <font color='#5AD66B'>joined</font>"
			+ " &middot; <font color='#D8D8D8'>open</font>"
			+ " &middot; <font color='#E05252'>blocked</font>"
			+ "</body></html>");
		hint.setFont(FontManager.getRunescapeSmallFont());
		hint.setForeground(ColorScheme.LIGHT_GRAY_COLOR);

		JPanel below = new JPanel(new BorderLayout(0, 4));
		below.setBackground(ColorScheme.DARK_GRAY_COLOR);
		below.add(hint, BorderLayout.NORTH);
		below.add(button("Line up with my house",
			"Slide this plan so it sits on top of the house you are standing in",
			e -> plugin.autoAlign()), BorderLayout.CENTER);
		below.add(roomEditor, BorderLayout.SOUTH);

		layout.add(top, BorderLayout.NORTH);
		layout.add(below, BorderLayout.CENTER);
		return layout;
	}

	private JButton button(String text, String tooltip, java.awt.event.ActionListener listener)
	{
		JButton button = new JButton(text);
		button.setToolTipText(tooltip);
		button.setFocusable(false);
		button.addActionListener(listener);
		return button;
	}

	// -------------------------------------------------------------------------------------------
	// Plan list
	// -------------------------------------------------------------------------------------------

	/**
	 * Reloads the plan drop-down from storage and reselects the active plan.
	 */
	public void rebuild()
	{
		if (plugin == null || grid == null)
		{
			return;
		}

		updatingCombo = true;
		try
		{
			templateCombo.removeAllItems();
			templateCombo.addItem(new ComboItem<>(null, "— no plan —"));

			HouseTemplate active = plugin.getActiveTemplate();
			List<HouseTemplate> stored = templateStore.getTemplates();
			for (HouseTemplate template : stored)
			{
				ComboItem<HouseTemplate> item = new ComboItem<>(template, template.getName());
				templateCombo.addItem(item);
				if (active != null && active.getId().equals(template.getId()))
				{
					templateCombo.setSelectedItem(item);
				}
			}

			if (active == null)
			{
				templateCombo.setSelectedIndex(0);
			}
		}
		finally
		{
			updatingCombo = false;
		}

		grid.setTemplate(plugin.getActiveTemplate());
		grid.setUnreachable(plugin.getUnreachableRooms());
		roomEditor.clear();
	}

	private void onTemplateSelected()
	{
		if (updatingCombo || plugin == null)
		{
			return;
		}
		Object selected = templateCombo.getSelectedItem();
		if (!(selected instanceof ComboItem))
		{
			return;
		}
		@SuppressWarnings("unchecked")
		HouseTemplate template = ((ComboItem<HouseTemplate>) selected).getValue();

		plugin.setActiveTemplate(template);
		grid.setTemplate(template);
		roomEditor.clear();
	}

	private void onCellSelected(int x, int y)
	{
		HouseTemplate template = plugin == null ? null : plugin.getActiveTemplate();
		if (template == null)
		{
			JOptionPane.showMessageDialog(this,
				"Make or pick a plan first.", "POH Templates", JOptionPane.INFORMATION_MESSAGE);
			grid.clearSelection();
			return;
		}
		roomEditor.select(template, grid.getPlane(), x, y);
		revalidate();
		repaint();
	}

	private void onPlanEdited()
	{
		HouseTemplate template = plugin == null ? null : plugin.getActiveTemplate();
		if (template == null)
		{
			return;
		}
		grid.setTemplate(template);
		grid.setUnreachable(plugin.getUnreachableRooms());
		plugin.planChanged();
		revalidate();
		repaint();
	}

	// -------------------------------------------------------------------------------------------
	// Plan actions
	// -------------------------------------------------------------------------------------------

	private void newPlan()
	{
		String name = JOptionPane.showInputDialog(this, "Name this plan:", "New plan");
		if (name == null || name.trim().isEmpty())
		{
			return;
		}
		HouseTemplate template = new HouseTemplate(name.trim());
		templateStore.put(template);
		plugin.setActiveTemplate(template);
		rebuild();
	}

	private void capture()
	{
		String name = JOptionPane.showInputDialog(this, "Name for the captured plan:", "My house");
		if (name == null || name.trim().isEmpty())
		{
			return;
		}
		final String trimmed = name.trim();

		plugin.runOnClientThread(() ->
		{
			final HouseTemplate captured = plugin.captureCurrentHouse(trimmed);
			SwingUtilities.invokeLater(() ->
			{
				if (captured.getRooms().isEmpty())
				{
					JOptionPane.showMessageDialog(this,
						"No house was found. Stand inside your house, and turn building mode on so "
							+ "the empty hotspots are visible too.",
						"POH Templates", JOptionPane.WARNING_MESSAGE);
					return;
				}
				templateStore.put(captured);
				plugin.setActiveTemplate(captured);
				rebuild();
				JOptionPane.showMessageDialog(this,
					"Captured " + captured.getRooms().size() + " rooms.",
					"POH Templates", JOptionPane.INFORMATION_MESSAGE);
			});
		});
	}

	private void importPlan()
	{
		JTextArea input = new JTextArea(6, 20);
		input.setLineWrap(true);
		input.setWrapStyleWord(true);

		int choice = JOptionPane.showConfirmDialog(this, new JScrollPane(input),
			"Paste a share code", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
		if (choice != JOptionPane.OK_OPTION)
		{
			return;
		}

		try
		{
			HouseTemplate imported = shareCodec.decode(input.getText()).copyWithNewId();
			templateStore.put(imported);
			plugin.setActiveTemplate(imported);
			rebuild();
			JOptionPane.showMessageDialog(this,
				"Imported \"" + imported.getName() + "\" with " + imported.getRooms().size() + " rooms.",
				"POH Templates", JOptionPane.INFORMATION_MESSAGE);
		}
		catch (ShareCodeException e)
		{
			log.debug("Rejected a share code", e);
			JOptionPane.showMessageDialog(this, e.getMessage(),
				"POH Templates", JOptionPane.ERROR_MESSAGE);
		}
	}

	private void exportPlan()
	{
		HouseTemplate template = plugin.getActiveTemplate();
		if (template == null)
		{
			JOptionPane.showMessageDialog(this, "Pick a plan first.",
				"POH Templates", JOptionPane.INFORMATION_MESSAGE);
			return;
		}

		try
		{
			String code = shareCodec.encode(template);
			Toolkit.getDefaultToolkit().getSystemClipboard().setContents(new StringSelection(code), null);

			JTextArea output = new JTextArea(code, 6, 20);
			output.setLineWrap(true);
			output.setWrapStyleWord(true);
			output.setEditable(false);
			output.selectAll();

			JOptionPane.showMessageDialog(this, new JScrollPane(output),
				"Share code (copied to your clipboard)", JOptionPane.PLAIN_MESSAGE);
		}
		catch (ShareCodeException e)
		{
			log.debug("Could not encode a plan", e);
			JOptionPane.showMessageDialog(this, e.getMessage(),
				"POH Templates", JOptionPane.ERROR_MESSAGE);
		}
		catch (IllegalStateException e)
		{
			log.debug("Clipboard was unavailable", e);
			JOptionPane.showMessageDialog(this,
				"Your clipboard is busy. Try the Export button again.",
				"POH Templates", JOptionPane.ERROR_MESSAGE);
		}
	}

	private void renamePlan()
	{
		HouseTemplate template = plugin.getActiveTemplate();
		if (template == null)
		{
			return;
		}
		String name = JOptionPane.showInputDialog(this, "New name:", template.getName());
		if (name == null || name.trim().isEmpty())
		{
			return;
		}
		template.setName(name.trim());
		templateStore.put(template);
		rebuild();
	}

	private void deletePlan()
	{
		HouseTemplate template = plugin.getActiveTemplate();
		if (template == null)
		{
			return;
		}
		int choice = JOptionPane.showConfirmDialog(this,
			"Delete \"" + template.getName() + "\"?", "POH Templates", JOptionPane.YES_NO_OPTION);
		if (choice != JOptionPane.YES_OPTION)
		{
			return;
		}
		templateStore.remove(template.getId());
		plugin.setActiveTemplate(null);
		rebuild();
	}

	// -------------------------------------------------------------------------------------------
	// Updates pushed from the plugin
	// -------------------------------------------------------------------------------------------

	/**
	 * Called on the Swing thread whenever the plan comparison has been recomputed.
	 */
	public void onProgressUpdated(@Nullable PlanProgress progress, @Nullable ShoppingList shoppingList)
	{
		if (buildSteps == null || shopping == null)
		{
			return;
		}
		buildSteps.update(progress);
		shopping.update(shoppingList);
		revalidate();
		repaint();
	}
}
