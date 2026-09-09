/*
 * Copyright (c) 2026, Roel
 * All rights reserved.
 * Licensed under the BSD 2-Clause License. See LICENSE for details.
 */
package com.pohtemplates.share;

import com.google.gson.Gson;
import com.pohtemplates.model.HouseTemplate;
import com.pohtemplates.model.PlannedRoom;
import java.util.Base64;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

public class ShareCodecTest
{
	private final ShareCodec codec = new ShareCodec(new Gson());

	private static HouseTemplate samplePlan()
	{
		HouseTemplate template = new HouseTemplate("Test plan");
		template.setAuthor("Tester");

		PlannedRoom garden = new PlannedRoom(1, 6, 6, "garden", 0);
		garden.getFurniture().put("centrepiece", "exit_portal");
		template.putRoom(garden);

		PlannedRoom parlour = new PlannedRoom(1, 6, 7, "parlour", 2);
		parlour.getFurniture().put("chair_1", "oak_chair");
		parlour.getFurniture().put("fireplace", "clay_fireplace");
		template.putRoom(parlour);

		return template;
	}

	@Test
	public void roundTripsAPlan() throws Exception
	{
		HouseTemplate original = samplePlan();
		HouseTemplate decoded = codec.decode(codec.encode(original));

		assertEquals(original.getName(), decoded.getName());
		assertEquals(original.getAuthor(), decoded.getAuthor());
		assertEquals(original.getRooms().size(), decoded.getRooms().size());

		PlannedRoom parlour = decoded.getRoomAt(1, 6, 7);
		assertNotNull(parlour);
		assertEquals("parlour", parlour.getRoom());
		assertEquals(2, parlour.getRotation());
		assertEquals("oak_chair", parlour.getFurniture().get("chair_1"));
	}

	@Test
	public void producesAPrefixedCode() throws Exception
	{
		assertTrue(codec.encode(samplePlan()).startsWith("POHT1-"));
	}

	@Test
	public void toleratesWhitespaceFromPastedCodes() throws Exception
	{
		String code = codec.encode(samplePlan());
		String mangled = code.substring(0, 20) + "\n  " + code.substring(20) + "\n";

		assertEquals(2, codec.decode(mangled).getRooms().size());
	}

	@Test
	public void rejectsSomethingThatIsNotAShareCode()
	{
		expectRejection("hello world");
		expectRejection("");
		expectRejection(null);
	}

	@Test
	public void rejectsADamagedCode()
	{
		expectRejection("POHT1-notvalidbase64!!!");
		expectRejection("POHT1-" + Base64.getUrlEncoder().withoutPadding()
			.encodeToString("not gzipped".getBytes(java.nio.charset.StandardCharsets.UTF_8)));
	}

	@Test
	public void dropsRoomsOutsideTheGrid() throws Exception
	{
		HouseTemplate template = samplePlan();
		template.getRooms().add(new PlannedRoom(1, 99, 4, "parlour", 0));
		template.getRooms().add(new PlannedRoom(7, 2, 2, "parlour", 0));

		assertEquals(2, codec.decode(codec.encode(template)).getRooms().size());
	}

	@Test
	public void normalisesRotation() throws Exception
	{
		HouseTemplate template = new HouseTemplate("Rotations");
		PlannedRoom room = new PlannedRoom(1, 3, 3, "parlour", 0);
		template.putRoom(room);

		HouseTemplate decoded = codec.decode(codec.encode(template));
		PlannedRoom decodedRoom = decoded.getRoomAt(1, 3, 3);
		assertNotNull(decodedRoom);
		assertTrue(decodedRoom.getRotation() >= 0 && decodedRoom.getRotation() <= 3);
	}

	@Test
	public void importedPlanGetsANewIdSoItCannotOverwriteAnExistingOne() throws Exception
	{
		HouseTemplate original = samplePlan();
		HouseTemplate imported = codec.decode(codec.encode(original)).copyWithNewId();

		assertTrue(!original.getId().equals(imported.getId()));
		assertEquals(original.getRooms().size(), imported.getRooms().size());
	}

	private void expectRejection(String code)
	{
		try
		{
			codec.decode(code);
			fail("expected " + code + " to be rejected");
		}
		catch (ShareCodeException expected)
		{
			assertNotNull(expected.getMessage());
		}
	}
}
