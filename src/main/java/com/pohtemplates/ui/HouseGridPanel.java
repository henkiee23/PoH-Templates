/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.data.Direction;
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
	/** Cell size the panel asks for. The grid shrinks below this rather than being clipped. */
	private static final int PREFERRED_CELL = 15;
	private static final int MIN_CELL = 10;
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
		setPreferredSize(square(PREFERRED_CELL));
		setMinimumSize(square(MIN_CELL));
		setMaximumSize(square(PREFERRED_CELL));
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

	private static Dimension square(int cell)
	{
		int side = GRID * cell + 1;
		return new Dimension(side, side);
	}

	/**
	 * The grid is drawn to fit whatever width it is given, so a scrollbar appearing beside it
	 * shrinks the squares instead of clipping the east edge off the house.
	 */
	private int cellSize()
	{
		int available = Math.min(getWidth(), getHeight()) - 1;
		return Math.max(MIN_CELL, Math.min(PREFERRED_CELL, available / GRID));
	}

	/** Left edge of the grid, so it stays centred when the panel is wider than the squares need. */
	private int originX()
	{
		return Math.max(0, (getWidth() - (GRID * cellSize() + 1)) / 2);
	}

	@Nullable
	private Point toCell(int px, int py)
	{
		int cell = cellSize();
		int left = originX();
		if (px < left)
		{
			return null;
		}
		int x = (px - left) / cell;
		// Screen y grows downwards, the house grid grows north, so flip it.
		int y = GRID - 1 - (py / cell);
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
		if (def == null)
		{
			return room.getRoom();
		}

		StringBuilder tip = new StringBuilder("<html>")
			.append(def.getName())
			.append(", facing ")
			.append(facing(room.getRotation()));

		for (Direction door : def.getDoors(room.getRotation()))
		{
			tip.append("<br>Door ")
				.append(door.name().toLowerCase())
				.append(": ")
				.append(describe(doorState(room, door)));
		}

		return tip.append("</html>").toString();
	}

	private static String describe(DoorState state)
	{
		switch (state)
		{
			case CONNECTED:
				return "joined to the room next door";
			case BLOCKED:
				return "blocked, the room next door has a wall here";
			case EDGE:
				return "faces off the edge of the grid";
			default:
				return "open, you can build here";
		}
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
			final int cell = cellSize();
			final int ox = originX();
			graphics.setFont(getFont().deriveFont(Font.BOLD, Math.max(8f, cell - 6f)));

			// Two passes. Doors sit on the cell edges, so everything that could paint over them —
			// the cell fills and the grid lines — has to go down first.
			for (int x = 0; x < GRID; x++)
			{
				for (int y = 0; y < GRID; y++)
				{
					int px = ox + x * cell;
					int py = (GRID - 1 - y) * cell;

					PlannedRoom room = template == null ? null : template.getRoomAt(plane, x, y);
					RoomDef def = room == null ? null : data.getRoom(room.getRoom());

					graphics.setColor(def == null ? EMPTY_CELL : def.toAwtColour());
					graphics.fillRect(px, py, cell, cell);

					graphics.setColor(GRID_LINE);
					graphics.drawRect(px, py, cell, cell);
				}
			}

			for (int x = 0; x < GRID; x++)
			{
				for (int y = 0; y < GRID; y++)
				{
					PlannedRoom room = template == null ? null : template.getRoomAt(plane, x, y);
					RoomDef def = room == null ? null : data.getRoom(room.getRoom());
					if (def != null)
					{
						drawRoom(graphics, ox + x * cell, (GRID - 1 - y) * cell, cell, def, room);
					}
				}
			}

			if (selected != null)
			{
				int px = ox + selected.x * cell;
				int py = (GRID - 1 - selected.y) * cell;
				graphics.setColor(SELECTION);
				graphics.setStroke(new BasicStroke(2f));
				graphics.drawRect(px + 1, py + 1, cell - 2, cell - 2);
			}
		}
		finally
		{
			graphics.dispose();
		}
	}

	/**
	 * How a door on one side of a room relates to whatever is on the other side of that wall.
	 */
	private enum DoorState
	{
		/** The neighbouring square has a room whose door lines up: the two are joined. */
		CONNECTED(new Color(0x5A, 0xD6, 0x6B)),
		/** The neighbouring square is empty, so this door is somewhere you can still build. */
		OPEN(new Color(0xD8, 0xD8, 0xD8)),
		/** There is a room next door, but its wall is solid on this side. */
		BLOCKED(new Color(0xE0, 0x52, 0x52)),
		/** The door faces off the edge of the house grid. */
		EDGE(new Color(0x70, 0x70, 0x70));

		private final Color colour;

		DoorState(Color colour)
		{
			this.colour = colour;
		}

		Color getColour()
		{
			return colour;
		}
	}

	private void drawRoom(Graphics2D graphics, int px, int py, int cell, RoomDef def, PlannedRoom room)
	{
		String initial = def.getName().substring(0, 1).toUpperCase();
		graphics.setColor(Color.WHITE);
		int textX = px + (cell - graphics.getFontMetrics().stringWidth(initial)) / 2;
		int textY = py + cell / 2 + graphics.getFontMetrics().getAscent() / 2 - 1;
		graphics.drawString(initial, textX, textY);

		// Doors sit on the cell edges, coloured by whether they actually join to anything. This is
		// also what shows the room's rotation, for every room whose doors are not symmetrical.
		for (Direction door : def.getDoors(room.getRotation()))
		{
			graphics.setColor(doorState(room, door).getColour());
			drawDoor(graphics, px, py, cell, door);
		}

		if (unreachable.contains(room))
		{
			graphics.setColor(WARNING);
			graphics.setStroke(new BasicStroke(1.5f));
			graphics.drawLine(px + 3, py + 3, px + cell - 3, py + cell - 3);
		}
	}

	private static void drawDoor(Graphics2D graphics, int px, int py, int cell, Direction door)
	{
		final int span = Math.max(4, cell / 2 - 1);
		final int thickness = 2;
		final int offset = (cell - span) / 2;

		switch (door)
		{
			case NORTH:
				graphics.fillRect(px + offset, py, span, thickness);
				break;
			case SOUTH:
				graphics.fillRect(px + offset, py + cell - thickness, span, thickness);
				break;
			case EAST:
				graphics.fillRect(px + cell - thickness, py + offset, thickness, span);
				break;
			default:
				graphics.fillRect(px, py + offset, thickness, span);
				break;
		}
	}

	/**
	 * @param door a door side that has already been rotated into grid space
	 */
	private DoorState doorState(PlannedRoom room, Direction door)
	{
		int nx = room.getX() + door.getDx();
		int ny = room.getY() + door.getDy();

		if (!HouseTemplate.inBounds(nx, ny))
		{
			return DoorState.EDGE;
		}

		PlannedRoom neighbour = template.getRoomAt(room.getPlane(), nx, ny);
		if (neighbour == null)
		{
			return DoorState.OPEN;
		}

		RoomDef neighbourDef = data.getRoom(neighbour.getRoom());
		if (neighbourDef == null)
		{
			return DoorState.OPEN;
		}

		return neighbourDef.getDoors(neighbour.getRotation()).contains(door.opposite())
			? DoorState.CONNECTED
			: DoorState.BLOCKED;
	}
}
