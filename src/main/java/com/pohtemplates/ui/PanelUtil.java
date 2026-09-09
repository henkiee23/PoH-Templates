/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Rectangle;
import javax.swing.BorderFactory;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JList;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.plaf.basic.BasicScrollBarUI;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.PluginPanel;

/**
 * Small helpers that keep this plugin's widgets looking like the rest of the client.
 */
final class PanelUtil
{
	/**
	 * The height RuneLite's own config panel gives its drop-downs.
	 */
	private static final int COMBO_HEIGHT = 22;

	/**
	 * Drop-downs are sized to the panel rather than to their longest entry. Left to itself a
	 * combo box asks for whatever width its widest item needs, which for a name like
	 * "Limestone spiral staircase" is far wider than the sidebar, and everything else then gets
	 * squeezed to fit it.
	 */
	private static final int COMBO_WIDTH = PluginPanel.PANEL_WIDTH - 24;

	/** Width the client's own look and feel gives its scrollbars. */
	private static final int SCROLLBAR_WIDTH = 7;

	private PanelUtil()
	{
	}

	/**
	 * @return a drop-down styled like the ones in RuneLite's own panels, which will not drag the
	 * panel wider than the sidebar however long its entries are
	 */
	static <T> JComboBox<T> comboBox()
	{
		JComboBox<T> box = new JComboBox<>();
		box.setFocusable(false);
		// Set the renderer before asking for a size: the combo runs the renderer over its items to
		// work out how wide it wants to be.
		box.setRenderer(new NullSafeRenderer());
		box.setPreferredSize(new Dimension(COMBO_WIDTH, COMBO_HEIGHT));
		box.setMinimumSize(new Dimension(60, COMBO_HEIGHT));
		box.setMaximumSize(new Dimension(Integer.MAX_VALUE, COMBO_HEIGHT));
		// The visible text gets clipped when it is too long, so the full value goes in the tooltip.
		box.addActionListener(e -> updateTooltip(box));
		return box;
	}

	static void updateTooltip(JComboBox<?> box)
	{
		Object selected = box.getSelectedItem();
		box.setToolTipText(selected == null ? null : selected.toString());
	}

	/**
	 * Gives the panel's scrollbar the same flat 7px grey look the rest of the client has.
	 * <p>
	 * The client's own look and feel already specifies this ({@code ScrollBar.width=7},
	 * {@code ScrollBar.thumb=@MEDIUM_GRAY}), but a panel that ends up with the platform default
	 * instead gets a wide, brightly coloured bar that neither matches nor fits. Painting it here
	 * makes the panel look right either way, and costs nothing when the client's own styling is
	 * already in place.
	 */
	static void styleScrollBar(JScrollPane scrollPane)
	{
		if (scrollPane == null)
		{
			return;
		}

		JScrollBar vertical = scrollPane.getVerticalScrollBar();
		vertical.setUI(new FlatScrollBarUI());
		vertical.setPreferredSize(new Dimension(SCROLLBAR_WIDTH, 0));
		// One click of the wheel moves a line, not a pixel.
		vertical.setUnitIncrement(16);

		scrollPane.setBorder(BorderFactory.createEmptyBorder());
	}

	/**
	 * A plain block thumb on a dark track, with no arrow buttons at the ends.
	 */
	private static final class FlatScrollBarUI extends BasicScrollBarUI
	{
		@Override
		protected void configureScrollBarColors()
		{
			thumbColor = ColorScheme.MEDIUM_GRAY_COLOR;
			trackColor = ColorScheme.SCROLL_TRACK_COLOR;
			thumbDarkShadowColor = ColorScheme.SCROLL_TRACK_COLOR;
			thumbHighlightColor = ColorScheme.MEDIUM_GRAY_COLOR;
			thumbLightShadowColor = ColorScheme.MEDIUM_GRAY_COLOR;
		}

		@Override
		protected void paintTrack(Graphics g, JComponent c, Rectangle bounds)
		{
			g.setColor(trackColor);
			g.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
		}

		@Override
		protected void paintThumb(Graphics g, JComponent c, Rectangle bounds)
		{
			if (bounds.isEmpty() || !scrollbar.isEnabled())
			{
				return;
			}
			g.setColor(isThumbRollover() ? ColorScheme.DARKER_GRAY_HOVER_COLOR : thumbColor);
			g.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
		}

		@Override
		protected JButton createDecreaseButton(int orientation)
		{
			return noButton();
		}

		@Override
		protected JButton createIncreaseButton(int orientation)
		{
			return noButton();
		}

		private static JButton noButton()
		{
			JButton button = new JButton();
			Dimension none = new Dimension(0, 0);
			button.setPreferredSize(none);
			button.setMinimumSize(none);
			button.setMaximumSize(none);
			return button;
		}
	}

	/**
	 * Matches the default list rendering the client uses, but survives the moment during a rebuild
	 * when a combo box has items but nothing selected yet.
	 */
	private static final class NullSafeRenderer extends DefaultListCellRenderer
	{
		@Override
		public Component getListCellRendererComponent(JList<?> list, Object value, int index,
			boolean isSelected, boolean cellHasFocus)
		{
			return super.getListCellRendererComponent(list, value == null ? "" : value.toString(),
				index, isSelected, cellHasFocus);
		}
	}
}
