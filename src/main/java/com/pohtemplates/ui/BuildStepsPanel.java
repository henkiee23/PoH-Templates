/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import com.pohtemplates.data.Material;
import com.pohtemplates.data.PohData;
import com.pohtemplates.game.BuildStep;
import com.pohtemplates.plan.PlanProgress;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.util.StringJoiner;
import javax.annotation.Nullable;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import net.runelite.client.ui.ColorScheme;
import net.runelite.client.ui.FontManager;
import net.runelite.client.ui.components.ProgressBar;

/**
 * The ordered list of everything left to do to turn the house into the plan.
 */
class BuildStepsPanel extends JPanel
{
	/** The list is informational; past this many rows it stops being readable and starts being slow. */
	private static final int MAX_ROWS = 60;

	private final PohData data;
	private final ProgressBar progressBar = new ProgressBar();
	private final JLabel status = new JLabel();
	private final JPanel steps = new JPanel();

	BuildStepsPanel(PohData data)
	{
		this.data = data;

		setLayout(new BorderLayout(0, 4));
		setBackground(ColorScheme.DARK_GRAY_COLOR);

		progressBar.setMaximumValue(100);
		progressBar.setBackground(ColorScheme.DARKER_GRAY_COLOR);
		progressBar.setForeground(ColorScheme.PROGRESS_INPROGRESS_COLOR);

		status.setFont(FontManager.getRunescapeSmallFont());
		status.setForeground(ColorScheme.LIGHT_GRAY_COLOR);

		JPanel header = new JPanel(new BorderLayout(0, 3));
		header.setBackground(ColorScheme.DARK_GRAY_COLOR);
		header.add(progressBar, BorderLayout.NORTH);
		header.add(status, BorderLayout.CENTER);

		steps.setLayout(new BoxLayout(steps, BoxLayout.Y_AXIS));
		steps.setBackground(ColorScheme.DARK_GRAY_COLOR);

		add(header, BorderLayout.NORTH);
		add(steps, BorderLayout.CENTER);
	}

	void update(@Nullable PlanProgress progress)
	{
		steps.removeAll();

		if (progress == null)
		{
			progressBar.setValue(0);
			progressBar.setCenterLabel("");
			status.setText("Pick a plan to see what to build.");
			steps.revalidate();
			steps.repaint();
			return;
		}

		int percent = (int) Math.round(progress.getFraction() * 100);
		progressBar.setValue(percent);
		progressBar.setCenterLabel(percent + "%");
		progressBar.setForeground(progress.isComplete()
			? ColorScheme.PROGRESS_COMPLETE_COLOR
			: ColorScheme.PROGRESS_INPROGRESS_COLOR);

		if (!progress.isHouseSeen())
		{
			status.setText("<html><body style='width:190px'>Visit your house to compare it with this plan. "
				+ "Everything below is listed as still to do.</body></html>");
		}
		else if (progress.isComplete())
		{
			status.setText("This plan is fully built.");
		}
		else
		{
			status.setText(progress.getMatchingRooms() + "/" + progress.getPlannedRooms() + " rooms, "
				+ progress.getMatchingFurniture() + "/" + progress.getPlannedFurniture() + " furniture");
		}

		int shown = 0;
		for (BuildStep step : progress.getSteps())
		{
			if (shown++ >= MAX_ROWS)
			{
				steps.add(plain("… and " + (progress.getSteps().size() - MAX_ROWS) + " more"));
				break;
			}
			steps.add(row(step));
		}

		steps.revalidate();
		steps.repaint();
	}

	private JPanel row(BuildStep step)
	{
		JPanel panel = new JPanel(new BorderLayout());
		panel.setBackground(ColorScheme.DARKER_GRAY_COLOR);
		panel.setBorder(BorderFactory.createEmptyBorder(3, 4, 3, 4));
		panel.setAlignmentX(Component.LEFT_ALIGNMENT);
		panel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 60));

		JLabel headline = new JLabel("<html><body style='width:180px'>"
			+ escape(step.describe()) + "</body></html>");
		headline.setFont(FontManager.getRunescapeSmallFont());
		headline.setForeground(ColorScheme.TEXT_COLOR);

		StringJoiner detail = new StringJoiner(", ");
		detail.add("lvl " + step.getLevelRequired());
		if (step.getCoinCost() > 0)
		{
			detail.add(String.format("%,d gp", step.getCoinCost()));
		}
		for (Material material : step.getMaterials())
		{
			detail.add(material.getQuantity() + "x " + itemName(material.getItemId()));
		}

		JLabel sub = new JLabel("<html><body style='width:180px'>" + escape(detail.toString()) + "</body></html>");
		sub.setFont(FontManager.getRunescapeSmallFont());
		sub.setForeground(ColorScheme.LIGHT_GRAY_COLOR);

		panel.add(headline, BorderLayout.NORTH);
		panel.add(sub, BorderLayout.CENTER);

		JPanel spaced = new JPanel(new BorderLayout());
		spaced.setBackground(ColorScheme.DARK_GRAY_COLOR);
		spaced.setBorder(BorderFactory.createEmptyBorder(0, 0, 3, 0));
		spaced.setAlignmentX(Component.LEFT_ALIGNMENT);
		spaced.setMaximumSize(new Dimension(Integer.MAX_VALUE, 66));
		spaced.add(panel, BorderLayout.CENTER);
		return spaced;
	}

	private String itemName(int itemId)
	{
		com.pohtemplates.data.ItemInfo info = data.getItem(itemId);
		return info == null || info.getName() == null ? "item " + itemId : info.getName();
	}

	private static JLabel plain(String text)
	{
		JLabel label = new JLabel(text);
		label.setFont(FontManager.getRunescapeSmallFont());
		label.setForeground(ColorScheme.LIGHT_GRAY_COLOR);
		label.setAlignmentX(Component.LEFT_ALIGNMENT);
		return label;
	}

	private static String escape(String text)
	{
		return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
	}
}
