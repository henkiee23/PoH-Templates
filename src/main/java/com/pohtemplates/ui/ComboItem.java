/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.ui;

import java.util.Objects;
import javax.annotation.Nullable;

/**
 * A combo box entry that shows {@code label} but carries {@code value}, so the drop-downs can offer
 * a "nothing selected" row without needing a null-tolerant renderer.
 */
class ComboItem<T>
{
	private final T value;
	private final String label;

	ComboItem(@Nullable T value, String label)
	{
		this.value = value;
		this.label = label;
	}

	@Nullable
	T getValue()
	{
		return value;
	}

	@Override
	public String toString()
	{
		return label;
	}

	@Override
	public boolean equals(Object o)
	{
		if (this == o)
		{
			return true;
		}
		if (!(o instanceof ComboItem))
		{
			return false;
		}
		ComboItem<?> that = (ComboItem<?>) o;
		return Objects.equals(value, that.value) && Objects.equals(label, that.label);
	}

	@Override
	public int hashCode()
	{
		return Objects.hash(value, label);
	}
}
