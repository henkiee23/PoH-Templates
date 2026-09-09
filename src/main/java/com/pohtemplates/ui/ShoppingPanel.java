/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.PohTemplatesConfig;
import com.pohtemplates.plan.ShoppingList;
import com.pohtemplates.plan.ShoppingListEntry;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import javax.annotation.Nullable;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.FontManager;

/**
 * Everything the outstanding steps need, priced at Grand Exchange rates, with a note on where an
 * ironman can get each item instead.
 */
class ShoppingPanel extends JPanel
{
	private final PohTemplatesConfig config;

	private final JLabel summary = new JLabel();
	private final JPanel entries = new JPanel();

	ShoppingPanel(PohTemplatesConfig config)
	{
		this.config = config;

		setLayout(new BorderLayout(0, 4));
		setBackground(ColorScheme.DARK_GRAY_COLOR);

		summary.setFont(FontManager.getRunescapeSmallFont());
		summary.setForeground(ColorScheme.TEXT_COLOR);

		entries.setLayout(new BoxLayout(entries, BoxLayout.Y_AXIS));
		entries.setBackground(ColorScheme.DARK_GRAY_COLOR);

		add(summary, BorderLayout.NORTH);
		add(entries, BorderLayout.CENTER);
	}

	void update(@Nullable ShoppingList list)
	{
		entries.removeAll();

		if (list == null)
		{
			summary.setText("Pick a plan to see what to buy.");
			entries.revalidate();
			entries.repaint();
			return;
		}

		if (list.isEmpty())
		{
			summary.setText("Nothing left to buy.");
			entries.revalidate();
			entries.repaint();
			return;
		}

		summary.setText("<html><body style='width:195px'>"
			+ "<b>" + formatGp(list.getTotalCost()) + "</b> total"
			+ "<br>" + formatGp(list.getMaterialCost()) + " in materials"
			+ "<br>" + formatGp(list.getCoinCost()) + " to the estate agent"
			+ "<br>Highest level needed: " + list.getHighestLevelNeeded()
			+ "</body></html>");

		boolean showSources = config.showIronmanSources();
		for (ShoppingListEntry entry : list.getEntries())
		{
			entries.add(row(entry, showSources));
		}

		entries.revalidate();
		entries.repaint();
	}

	private JPanel row(ShoppingListEntry entry, boolean showSources)
	{
		JPanel inner = new JPanel(new BorderLayout());
		inner.setBackground(ColorScheme.DARKER_GRAY_COLOR);
		inner.setBorder(BorderFactory.createEmptyBorder(3, 4, 3, 4));

		JLabel headline = new JLabel("<html><body style='width:180px'>"
			+ String.format("%,d", entry.getQuantity()) + " &times; " + escape(entry.getName())
			+ "</body></html>");
		headline.setFont(FontManager.getRunescapeSmallFont());
		headline.setForeground(ColorScheme.TEXT_COLOR);
		inner.add(headline, BorderLayout.NORTH);

		String priceText = entry.isTradeable()
			? formatGp(entry.getTotalPrice()) + "  (" + formatGp(entry.getUnitPrice()) + " ea)"
			: "Not tradeable";
		JLabel price = new JLabel(priceText);
		price.setFont(FontManager.getRunescapeSmallFont());
		price.setForeground(entry.isTradeable()
			? ColorScheme.GRAND_EXCHANGE_PRICE
			: ColorScheme.LIGHT_GRAY_COLOR);
		inner.add(price, BorderLayout.CENTER);

		if (showSources && !entry.getSources().isEmpty())
		{
			StringBuilder sources = new StringBuilder("<html><body style='width:180px'>");
			for (String source : entry.getSources())
			{
				sources.append("• ").append(escape(source)).append("<br>");
			}
			sources.append("</body></html>");

			JLabel sourceLabel = new JLabel(sources.toString());
			sourceLabel.setFont(FontManager.getRunescapeSmallFont());
			sourceLabel.setForeground(ColorScheme.LIGHT_GRAY_COLOR);
			sourceLabel.setBorder(BorderFactory.createEmptyBorder(2, 0, 0, 0));
			inner.add(sourceLabel, BorderLayout.SOUTH);
		}

		JPanel spaced = new JPanel(new BorderLayout());
		spaced.setBackground(ColorScheme.DARK_GRAY_COLOR);
		spaced.setBorder(BorderFactory.createEmptyBorder(0, 0, 3, 0));
		spaced.setAlignmentX(Component.LEFT_ALIGNMENT);
		spaced.setMaximumSize(new Dimension(Integer.MAX_VALUE, 220));
		spaced.add(inner, BorderLayout.CENTER);
		return spaced;
	}

	private static String formatGp(long amount)
	{
		return String.format("%,d gp", amount);
	}

	private static String escape(String text)
	{
		return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
	}
}
