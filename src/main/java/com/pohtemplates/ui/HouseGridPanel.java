/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.data.PohData;
import com.pohtemplates.data.RoomDef;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.RenderingHints;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Set;
import java.util.function.BiConsumer;
import javax.annotation.Nullable;
import javax.swing.JPanel;
import javax.swing.ToolTipManager;
import net.runelite.client.ui.ColorScheme;

/**
 * The 13x13 house grid for one floor. Click a square to select it; the editor below the grid then
 * shows what can go there.
 */
class HouseGridPanel extends JPanel
{
	private static final int GRID = HouseTemplate.GRID_SIZE;
	private static final int CELL = 16;
	private static final Color GRID_LINE = new Color(60, 60, 60);
	private static final Color EMPTY_CELL = new Color(38, 38, 38);
	private static final Color SELECTION = new Color(255, 255, 255, 220);
	private static final Color WARNING = new Color(230, 80, 80);

	private final PohData data;
	private final BiConsumer<Integer, Integer> onCellSelected;

	private HouseTemplate template;
	private int plane = 1;
	private Point selected;
	private Set<PlannedRoom> unreachable = java.util.Collections.emptySet();

	HouseGridPanel(PohData data, BiConsumer<Integer, Integer> onCellSelected)
	{
		this.data = data;
		this.onCellSelected = onCellSelected;

		setBackground(ColorScheme.DARKER_GRAY_COLOR);
		int size = GRID * CELL + 1;
		setPreferredSize(new Dimension(size, size));
		setMinimumSize(new Dimension(size, size));
		setMaximumSize(new Dimension(size, size));
		ToolTipManager.sharedInstance().registerComponent(this);

		addMouseListener(new MouseAdapter()
		{
			@Override
			public void mousePressed(MouseEvent e)
			{
				Point cell = toCell(e.getX(), e.getY());
				if (cell == null)
				{
					return;
				}
				selected = cell;
				repaint();
				onCellSelected.accept(cell.x, cell.y);
			}
		});
	}

	void setTemplate(@Nullable HouseTemplate template)
	{
		this.template = template;
		repaint();
	}

	void setPlane(int plane)
	{
		this.plane = plane;
		this.selected = null;
		repaint();
	}

	int getPlane()
	{
		return plane;
	}

	void setUnreachable(Set<PlannedRoom> unreachable)
	{
		this.unreachable = unreachable == null ? java.util.Collections.emptySet() : unreachable;
		repaint();
	}

	@Nullable
	Point getSelected()
	{
		return selected;
	}

	void clearSelection()
	{
		selected = null;
		repaint();
	}

	@Nullable
	private Point toCell(int px, int py)
	{
		int x = px / CELL;
		// Screen y grows downwards, the house grid grows north, so flip it.
		int y = GRID - 1 - (py / CELL);
		return HouseTemplate.inBounds(x, y) ? new Point(x, y) : null;
	}

	@Override
	public String getToolTipText(MouseEvent event)
	{
		Point cell = toCell(event.getX(), event.getY());
		if (cell == null || template == null)
		{
			return null;
		}
		PlannedRoom room = template.getRoomAt(plane, cell.x, cell.y);
		if (room == null)
		{
			return "Empty (" + cell.x + ", " + cell.y + ")";
		}
		RoomDef def = data.getRoom(room.getRoom());
		String name = def == null ? room.getRoom() : def.getName();
		return name + " facing " + facing(room.getRotation());
	}

	private static String facing(int rotation)
	{
		switch (((rotation % 4) + 4) % 4)
		{
			case 1:
				return "east";
			case 2:
				return "south";
			case 3:
				return "west";
			default:
				return "north";
		}
	}

	@Override
	protected void paintComponent(Graphics g)
	{
		super.paintComponent(g);
		Graphics2D graphics = (Graphics2D) g.create();
		try
		{
			graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
			graphics.setFont(getFont().deriveFont(Font.BOLD, 9f));

			for (int x = 0; x < GRID; x++)
			{
				for (int y = 0; y < GRID; y++)
				{
					int px = x * CELL;
					int py = (GRID - 1 - y) * CELL;

					PlannedRoom room = template == null ? null : template.getRoomAt(plane, x, y);
					RoomDef def = room == null ? null : data.getRoom(room.getRoom());

					graphics.setColor(def == null ? EMPTY_CELL : def.toAwtColour());
					graphics.fillRect(px, py, CELL, CELL);

					if (def != null)
					{
						drawRoom(graphics, px, py, def, room);
					}

					graphics.setColor(GRID_LINE);
					graphics.drawRect(px, py, CELL, CELL);
				}
			}

			if (selected != null)
			{
				int px = selected.x * CELL;
				int py = (GRID - 1 - selected.y) * CELL;
				graphics.setColor(SELECTION);
				graphics.setStroke(new BasicStroke(2f));
				graphics.drawRect(px + 1, py + 1, CELL - 2, CELL - 2);
			}
		}
		finally
		{
			graphics.dispose();
		}
	}

	private void drawRoom(Graphics2D graphics, int px, int py, RoomDef def, PlannedRoom room)
	{
		// A tick on the side the room faces, so rotation is visible at a glance.
		graphics.setColor(Color.WHITE);
		switch (((room.getRotation() % 4) + 4) % 4)
		{
			case 1:
				graphics.fillRect(px + CELL - 3, py + 6, 2, 4);
				break;
			case 2:
				graphics.fillRect(px + 6, py + CELL - 3, 4, 2);
				break;
			case 3:
				graphics.fillRect(px + 1, py + 6, 2, 4);
				break;
			default:
				graphics.fillRect(px + 6, py + 1, 4, 2);
				break;
		}

		String initial = def.getName().substring(0, 1).toUpperCase();
		graphics.setColor(Color.WHITE);
		int textX = px + (CELL - graphics.getFontMetrics().stringWidth(initial)) / 2;
		int textY = py + CELL / 2 + 4;
		graphics.drawString(initial, textX, textY);

		if (unreachable.contains(room))
		{
			graphics.setColor(WARNING);
			graphics.setStroke(new BasicStroke(1.5f));
			graphics.drawLine(px + 2, py + 2, px + CELL - 2, py + CELL - 2);
		}
	}
}
