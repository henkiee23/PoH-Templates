/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.data.FurnitureDef;
import com.pohtemplates.data.HotspotDef;
import com.pohtemplates.data.PohData;
import com.pohtemplates.data.RoomDef;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.Nullable;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.FontManager;

/**
 * Edits the room in the square the user picked on the grid: which room it is, which way it faces,
 * and what goes in each of its hotspots.
 */
class RoomEditorPanel extends JPanel
{
	private static final String NO_ROOM = "— empty —";
	private static final String NO_FURNITURE = "— leave empty —";
	private static final String[] FACINGS = {"north", "east", "south", "west"};

	private final PohData data;
	private final Runnable onChanged;

	private final JLabel title = new JLabel();
	private final JComboBox<ComboItem<RoomDef>> roomCombo = PanelUtil.comboBox();
	private final JButton rotateButton = new JButton();
	private final JPanel hotspotPanel = new JPanel();

	private HouseTemplate template;
	private int plane;
	private int x;
	private int y;
	private boolean updating;

	RoomEditorPanel(PohData data, Runnable onChanged)
	{
		this.data = data;
		this.onChanged = onChanged;

		setLayout(new BorderLayout(0, 4));
		setBackground(ColorScheme.DARK_GRAY_COLOR);
		setBorder(BorderFactory.createEmptyBorder(4, 0, 0, 0));

		title.setFont(FontManager.getRunescapeBoldFont());
		title.setForeground(ColorScheme.BRAND_ORANGE);

		roomCombo.addActionListener(e -> onRoomChosen());

		rotateButton.setFocusable(false);
		rotateButton.addActionListener(e -> rotate());

		JPanel top = new JPanel(new BorderLayout(0, 3));
		top.setBackground(ColorScheme.DARK_GRAY_COLOR);
		top.add(title, BorderLayout.NORTH);

		JPanel controls = new JPanel(new GridLayout(2, 1, 0, 3));
		controls.setBackground(ColorScheme.DARK_GRAY_COLOR);
		controls.add(roomCombo);
		controls.add(rotateButton);
		top.add(controls, BorderLayout.CENTER);

		hotspotPanel.setLayout(new BoxLayout(hotspotPanel, BoxLayout.Y_AXIS));
		hotspotPanel.setBackground(ColorScheme.DARK_GRAY_COLOR);

		add(top, BorderLayout.NORTH);
		add(hotspotPanel, BorderLayout.CENTER);

		setVisible(false);
	}

	/**
	 * Points the editor at a grid square. Pass {@code null} to hide it.
	 */
	void select(@Nullable HouseTemplate template, int plane, int x, int y)
	{
		this.template = template;
		this.plane = plane;
		this.x = x;
		this.y = y;

		if (template == null)
		{
			setVisible(false);
			return;
		}

		setVisible(true);
		updating = true;
		try
		{
			title.setText("Square " + x + ", " + y);
			rebuildRoomCombo();
		}
		finally
		{
			updating = false;
		}
		rebuildHotspots();
	}

	void clear()
	{
		template = null;
		setVisible(false);
	}

	private void rebuildRoomCombo()
	{
		roomCombo.removeAllItems();
		roomCombo.addItem(new ComboItem<>(null, NO_ROOM));

		PlannedRoom planned = template.getRoomAt(plane, x, y);
		String currentId = planned == null ? null : planned.getRoom();

		for (RoomDef room : data.getRooms())
		{
			if (!room.allowsPlane(plane))
			{
				continue;
			}
			ComboItem<RoomDef> item = new ComboItem<>(room, room.getName() + "  (lvl " + room.getLevel() + ")");
			roomCombo.addItem(item);
			if (room.getId().equals(currentId))
			{
				roomCombo.setSelectedItem(item);
			}
		}

		if (currentId == null)
		{
			roomCombo.setSelectedIndex(0);
		}

		updateRotateButton(planned);
	}

	private void updateRotateButton(@Nullable PlannedRoom planned)
	{
		if (planned == null)
		{
			rotateButton.setText("Facing —");
			rotateButton.setEnabled(false);
		}
		else
		{
			rotateButton.setText("Facing " + FACINGS[planned.getRotation()] + "  ↻");
			rotateButton.setEnabled(true);
		}
	}

	private void onRoomChosen()
	{
		if (updating || template == null)
		{
			return;
		}

		Object selected = roomCombo.getSelectedItem();
		if (!(selected instanceof ComboItem))
		{
			return;
		}

		@SuppressWarnings("unchecked")
		RoomDef room = ((ComboItem<RoomDef>) selected).getValue();

		if (room == null)
		{
			template.removeRoomAt(plane, x, y);
		}
		else
		{
			PlannedRoom existing = template.getRoomAt(plane, x, y);
			int rotation = existing == null ? 0 : existing.getRotation();
			if (existing != null && room.getId().equals(existing.getRoom()))
			{
				return;
			}
			template.putRoom(new PlannedRoom(plane, x, y, room.getId(), rotation));
		}

		updateRotateButton(template.getRoomAt(plane, x, y));
		rebuildHotspots();
		onChanged.run();
	}

	private void rotate()
	{
		PlannedRoom planned = template == null ? null : template.getRoomAt(plane, x, y);
		if (planned == null)
		{
			return;
		}
		planned.setRotation(planned.getRotation() + 1);
		updateRotateButton(planned);
		onChanged.run();
	}

	private void rebuildHotspots()
	{
		hotspotPanel.removeAll();

		PlannedRoom planned = template == null ? null : template.getRoomAt(plane, x, y);
		RoomDef room = planned == null ? null : data.getRoom(planned.getRoom());

		if (room != null)
		{
			if (room.getNote() != null && !room.getNote().isEmpty())
			{
				hotspotPanel.add(note(room.getNote()));
			}

			for (HotspotDef hotspot : room.getHotspots())
			{
				hotspotPanel.add(buildHotspotRow(planned, hotspot));
			}
		}

		hotspotPanel.revalidate();
		hotspotPanel.repaint();
	}

	private JLabel note(String text)
	{
		JLabel label = new JLabel("<html><body style='width:190px'>" + escape(text) + "</body></html>");
		label.setFont(FontManager.getRunescapeSmallFont());
		label.setForeground(ColorScheme.LIGHT_GRAY_COLOR);
		label.setBorder(BorderFactory.createEmptyBorder(2, 0, 4, 0));
		label.setAlignmentX(Component.LEFT_ALIGNMENT);
		return label;
	}

	private JPanel buildHotspotRow(PlannedRoom planned, HotspotDef hotspot)
	{
		JPanel row = new JPanel(new BorderLayout(0, 1));
		row.setBackground(ColorScheme.DARK_GRAY_COLOR);
		row.setBorder(BorderFactory.createEmptyBorder(3, 0, 0, 0));
		row.setAlignmentX(Component.LEFT_ALIGNMENT);
		row.setMaximumSize(new Dimension(Integer.MAX_VALUE, 46));

		JLabel label = new JLabel(hotspot.getName());
		label.setFont(FontManager.getRunescapeSmallFont());
		label.setForeground(ColorScheme.TEXT_COLOR);
		row.add(label, BorderLayout.NORTH);

		JComboBox<ComboItem<FurnitureDef>> combo = PanelUtil.comboBox();
		combo.addItem(new ComboItem<>(null, NO_FURNITURE));

		String currentId = planned.getFurniture().get(hotspot.getId());
		List<ComboItem<FurnitureDef>> items = new ArrayList<>();
		for (FurnitureDef option : hotspot.getOptions())
		{
			ComboItem<FurnitureDef> item = new ComboItem<>(option, option.getName() + "  (" + option.getLevel() + ")");
			items.add(item);
			combo.addItem(item);
		}

		if (currentId != null)
		{
			for (ComboItem<FurnitureDef> item : items)
			{
				FurnitureDef value = item.getValue();
				if (value != null && currentId.equals(value.getId()))
				{
					combo.setSelectedItem(item);
					break;
				}
			}
		}

		combo.addActionListener(e ->
		{
			Object selected = combo.getSelectedItem();
			if (!(selected instanceof ComboItem))
			{
				return;
			}
			@SuppressWarnings("unchecked")
			FurnitureDef furniture = ((ComboItem<FurnitureDef>) selected).getValue();

			if (furniture == null)
			{
				planned.getFurniture().remove(hotspot.getId());
			}
			else
			{
				planned.getFurniture().put(hotspot.getId(), furniture.getId());
			}
			onChanged.run();
		});

		row.add(combo, BorderLayout.CENTER);
		return row;
	}

	private static String escape(String text)
	{
		return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
	}
}
