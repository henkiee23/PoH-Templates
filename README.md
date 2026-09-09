# POH Templates

A RuneLite plugin for planning your player-owned house.

Draw the layout you want — which room goes in which square, which way it faces, and what furniture
goes in each hotspot — and the plugin works out what you still have to build, what it will cost, and
where to get the materials. While you are in building mode it outlines the hotspots your plan wants
something in and tells you what to build there.

Plans are shared as text codes, so you can hand one to a friend or paste one into a planner website.

## What it does

**Plan the layout.** A 13x13 grid per floor (dungeon, ground, first floor). Click a square, pick a
room and which way it faces, then choose what goes in each of its hotspots.

Each room shows its doors on the edges of its square, coloured by what is on the other side:
**green** where two rooms' doors line up and the pair is joined, **grey** where the door faces an
empty square you could still build on, and **red** where the neighbouring room has a solid wall
there. A room that joins nothing gets a red cross. Because doors turn with the room, they also show
you which way it is facing. Hovering a square spells all of this out.

**See what is left.** Stand in your house and the plugin compares it against your plan: which rooms
are missing, which are turned the wrong way, and which hotspots are empty or hold the wrong thing.
The list is ordered so you can work down it.

**Get a shopping list.** Every outstanding step is rolled up into a materials list priced at Grand
Exchange rates, with the estate agent's room fees totalled separately. Each material also lists where
to buy or make it without the Grand Exchange, which is the part ironmen actually need. Nails get a
configurable margin because they bend.

**Be shown where to build.** In building mode the hotspots your plan still wants something in are
outlined, labelled with what to build. Hotspots that already hold the wrong item are outlined in a
different colour.

**Share plans.** Export gives you a `POHT1-…` code on your clipboard. Import takes one back. There is
no network access anywhere in the plugin: sharing is copy and paste.

## Getting started

1. Enable **POH Templates** and open its panel from the sidebar.
2. Go to your house and turn on building mode, so the plugin can see the empty hotspots too.
3. Press **Capture** to turn your current house into a plan, or **New** to start from nothing.
4. Edit the layout on the **Layout** tab, then check **To build** and **Shopping**.

If you imported someone else's plan, press **Line up with my house** — it slides the plan across the
grid until it sits on top of your actual rooms, so the comparison lines up.

## Settings

| Setting | What it does |
| --- | --- |
| Highlight build hotspots | Outline hotspots your plan wants something in |
| Show labels | Write what to build next to each outlined hotspot |
| To build / Wrong item built | Outline colours |
| Only show what I can build | Hide hotspots above your current Construction level |
| Highlight range | How far away a hotspot can be and still be outlined |
| Spare nails | Margin added to nails on the shopping list, since they bend |
| Show ironman sources | List where each material can be bought or made |

## Room coverage

The bundled data currently covers **garden, parlour, kitchen, dining room, bedroom and hall (skill
trophies)** — 43 hotspots, 194 buildable items and a door layout for each room. Rooms that are not in
the data yet simply do not appear in the room picker; nothing breaks.

Adding a room is a data change, not a code change. See below.

## How the data is put together

`src/main/resources/com/pohtemplates/rooms.json` is generated, never edited by hand. Two independent
sources feed it, and they are deliberately kept apart:

- **Object ids** come from the game cache, via the generated `net.runelite.api.gameval.ObjectID`
  constants. These identify empty hotspots and built furniture in the scene, and are what house
  detection relies on.
- **Construction levels, materials and experience** come from the [OSRS Wiki](https://oldschool.runescape.wiki/w/Construction).
- **Door layouts** come from the `doors` parameter of each room page's `Infobox Room` template
  (fetch a page with `?action=raw` to see it), which gives them as a compact `nesw` string rather
  than only as the rendered image.

Within a hotspot the cache numbers furniture in the same order the wiki lists it by level
(`POH_CHAIR1` … `POH_CHAIR7` are the seven parlour chairs in level order), which is what makes the
two sides checkable against each other.

To add a room:

1. Add its furniture to `FURNITURE` in `tools/build_data.py`, one entry per buildable option.
2. Add the room to `ROOMS`, with its `doors`, each hotspot's empty-hotspot object ids, and the
   furniture family each hotspot uses.
3. `python3 tools/build_data.py` to regenerate, then `python3 tools/validate_data.py` to check it.

The validator refuses ids that mean two different hotspots in one room, object ids that are listed as
both an empty hotspot and built furniture, materials with no entry in the item table, and levels
outside 1–99. `PohDataTest` runs the same checks as part of the build.

## Building

```
./gradlew build          # compile and run the tests
./gradlew run            # launch a development client with the plugin loaded
```

Requires JDK 11 or later. To sign in to the development client, follow
[Using Jagex Accounts](https://github.com/runelite/runelite/wiki/Using-Jagex-Accounts).

## Design notes

**No automation.** The plugin only ever draws on top of what the client already shows. It never adds
or changes menu entries, never sends input, and never acts on your behalf. Construction menu
modification is explicitly forbidden for hub plugins, and this plugin does not go near it.

**No network access.** Prices come from RuneLite's own item price cache. Sharing is copy and paste.
There is no third-party server, so there is nothing to opt in to.

**Untrusted input is treated as untrusted.** A pasted share code is bounded in length, capped when it
inflates, and bounds-checked field by field before anything is done with it. An imported plan always
gets a fresh id so it cannot silently overwrite one you already have.

**The scene is not swept.** Rooms are built up from object spawn and despawn events and thrown away
when a new scene loads, so nothing walks the scene per tick or per frame.

## Known gaps

- Only the six rooms listed above are in the data so far.
- A few furniture pieces have no object id yet (cat baskets, dressers, staircases). The plugin still
  shows their hotspot and counts them in the shopping list; it just cannot tell that one is already
  built, so it will keep listing them as outstanding.
- Rooms are matched to grid squares by scene chunk. That is stable for your own house; imported plans
  may need **Line up with my house** once.
- Door sides are taken to be in the same orientation the game's room template uses. That is the
  assumption the wiki's own door-layout diagrams are drawn in, but it has not been checked against a
  real house yet — if doors appear on the wrong walls after capturing your house, that is why.

## Licence

BSD 2-Clause. See [LICENSE](LICENSE).

Not affiliated with Jagex. Old School RuneScape is a trademark of Jagex Ltd.
