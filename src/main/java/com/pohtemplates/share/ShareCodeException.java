/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.share;

/**
 * Thrown when a share code cannot be read. The message is shown to the user, so keep it plain.
 */
public class ShareCodeException extends Exception
{
	public ShareCodeException(String message)
	{
		super(message);
	}

	public ShareCodeException(String message, Throwable cause)
	{
		super(message, cause);
	}
}
