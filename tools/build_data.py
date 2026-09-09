#!/usr/bin/env python3
"""
Generates src/main/resources/com/pohtemplates/rooms.json.

Two sources feed this file, and they are kept apart on purpose:

* Object ids come from the game cache, via the generated constants in
  net.runelite.api.gameval.ObjectID / ObjectID1. They are authoritative.
* Construction levels, materials and experience come from the OSRS Wiki.

Within a hotspot family the cache numbers furniture in the same order the wiki
lists it by level, so FURNITURE entries carry their object ids inline and the
two stay checkable side by side.

Run:  python3 tools/build_data.py
"""

import json
import os

OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "main", "resources", "com", "pohtemplates", "rooms.json",
)

FORMAT = 1

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

PLANK = 960
OAK_PLANK = 8778
TEAK_PLANK = 8780
MAHOGANY_PLANK = 8782
NAILS = 1539            # Steel nails; any nail type works, quality only changes how many bend.
BOLT_OF_CLOTH = 8790
SOFT_CLAY = 1761
LIMESTONE_BRICK = 3420
MARBLE_BLOCK = 8786
GOLD_LEAF = 8784
MAGIC_STONE = 8788
MOLTEN_GLASS = 1775
STEEL_BAR = 2353
IRON_BAR = 2351
WOOL = 1737
CONDENSED_GOLD = 26266
PLATINUM_TOKEN = 13204
TEA_LEAVES = 7738

BAGGED_PLANT_1 = 8431
BAGGED_PLANT_2 = 8433
BAGGED_PLANT_3 = 8435
BAGGED_DEAD_TREE = 8417
BAGGED_NICE_TREE = 8419
BAGGED_OAK_TREE = 8421
BAGGED_WILLOW_TREE = 8423
BAGGED_MAPLE_TREE = 8425
BAGGED_YEW_TREE = 8427
BAGGED_MAGIC_TREE = 8429

SAWMILL = "Sawmill operator (Varrock, Woodcutting Guild, Prifddinas, Port Khazard, Farming Guild)"
CONSTRUCTION_SUPPLIES = "Construction Supplies shop (sawmill operator NE of Varrock, or the Woodcutting Guild)"
RAZMIRE = "Razmire Builders Merchants, Mort'ton"
STONEMASON = "Keldagrim Stonemason, or Stonecutter Supplies at the Stonecutter Outpost"

ITEM_INFO = [
    dict(itemId=PLANK, name="Plank", sources=[
        SAWMILL + " - 100 coins per regular log",
        RAZMIRE,
        "Plank Make spell (86 Magic)",
    ]),
    dict(itemId=OAK_PLANK, name="Oak plank", sources=[
        SAWMILL + " - 250 coins per oak log",
        "Plank Make spell (86 Magic)",
    ]),
    dict(itemId=TEAK_PLANK, name="Teak plank", sources=[
        SAWMILL + " - 500 coins per teak log",
        "Plank Make spell (86 Magic)",
    ]),
    dict(itemId=MAHOGANY_PLANK, name="Mahogany plank", sources=[
        SAWMILL + " - 1,500 coins per mahogany log",
        "Plank Make spell (86 Magic)",
    ]),
    dict(itemId=NAILS, name="Steel nails", sources=[
        CONSTRUCTION_SUPPLIES,
        "Smith them: 1 steel bar makes 15 nails (34 Smithing)",
        "Any nail type works. Better nails bend less often, so you need fewer spares",
    ]),
    dict(itemId=BOLT_OF_CLOTH, name="Bolt of cloth", sources=[CONSTRUCTION_SUPPLIES]),
    dict(itemId=SOFT_CLAY, name="Soft clay", sources=[
        "Use a bucket or jug of water on clay",
        "Humidify spell (68 Magic) on clay",
        "Mine clay while wearing a bracelet of clay",
        "Soft clay packs from Prospector Percy at the Motherlode Mine, 10 nuggets for 100",
    ]),
    dict(itemId=LIMESTONE_BRICK, name="Limestone brick", sources=[
        "Chisel limestone (12 Crafting). Limestone is mined at the Paterdomus quarry",
        RAZMIRE,
        STONEMASON,
    ]),
    dict(itemId=MARBLE_BLOCK, name="Marble block", sources=[STONEMASON]),
    dict(itemId=GOLD_LEAF, name="Gold leaf", sources=[STONEMASON]),
    dict(itemId=MAGIC_STONE, name="Magic stone", sources=[STONEMASON]),
    dict(itemId=CONDENSED_GOLD, name="Condensed gold", sources=[STONEMASON]),
    dict(itemId=MOLTEN_GLASS, name="Molten glass", sources=[
        "Use a bucket of sand and soda ash on a furnace (1 Crafting)",
        "Superglass Make spell (77 Magic)",
    ]),
    dict(itemId=STEEL_BAR, name="Steel bar", sources=[
        "Smelt 1 iron ore and 2 coal (30 Smithing)",
        "Blast Furnace, which halves the coal needed",
    ]),
    dict(itemId=IRON_BAR, name="Iron bar", sources=["Smelt iron ore (15 Smithing)"]),
    dict(itemId=WOOL, name="Wool", sources=["Shear a sheep, e.g. at Fred's farm north of Lumbridge"]),
    dict(itemId=PLATINUM_TOKEN, name="Platinum token", sources=[
        "Exchange 1,000,000 coins at a bank",
    ]),
    dict(itemId=TEA_LEAVES, name="Tea leaves", sources=["Any larder in your kitchen"]),
    dict(itemId=BAGGED_PLANT_1, name="Bagged plant 1", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_PLANT_2, name="Bagged plant 2", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_PLANT_3, name="Bagged plant 3", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_DEAD_TREE, name="Bagged dead tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_NICE_TREE, name="Bagged nice tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_OAK_TREE, name="Bagged oak tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_WILLOW_TREE, name="Bagged willow tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_MAPLE_TREE, name="Bagged maple tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_YEW_TREE, name="Bagged yew tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
    dict(itemId=BAGGED_MAGIC_TREE, name="Bagged magic tree", sources=["Garden supplier stalls, or the Grand Exchange"]),
]

# ---------------------------------------------------------------------------
# House styles
# ---------------------------------------------------------------------------

STYLES = [
    dict(id="basic_wood", name="Basic wood", level=1, cost=5000),
    dict(id="basic_stone", name="Basic stone", level=10, cost=5000),
    dict(id="whitewashed_stone", name="Whitewashed stone", level=20, cost=7500),
    dict(id="fremennik_wood", name="Fremennik-style wood", level=30, cost=10000),
    dict(id="tropical_wood", name="Tropical wood", level=40, cost=15000),
    dict(id="fancy_stone", name="Fancy stone", level=50, cost=25000),
    dict(id="deathly_mansion", name="Deathly mansion", level=60, cost=100000,
         note="Unlocked by the Daddy's Home miniquest"),
    dict(id="twisted", name="Twisted", level=1, cost=0, note="Cosmetic override, unlocked from a league"),
    dict(id="hosidius", name="Hosidius", level=1, cost=0, note="Cosmetic override"),
]


def m(item, qty=1):
    return dict(itemId=item, quantity=qty)


# ---------------------------------------------------------------------------
# Furniture, grouped by hotspot family so rooms with several identical hotspots
# (a parlour has three chair spaces) share one list.
# ---------------------------------------------------------------------------

FURNITURE = {
    # --- Parlour -----------------------------------------------------------
    "parlour_chair": [
        dict(id="crude_wooden_chair", name="Crude wooden chair", level=1, xp=58,
             materials=[m(PLANK, 2), m(NAILS, 2)], objectIds=[6752]),
        dict(id="wooden_chair", name="Wooden chair", level=8, xp=87,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[6753]),
        dict(id="rocking_chair", name="Rocking chair", level=14, xp=87,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[6754]),
        dict(id="oak_chair", name="Oak chair", level=19, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[6755]),
        dict(id="oak_armchair", name="Oak armchair", level=26, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[6756]),
        dict(id="teak_armchair", name="Teak armchair", level=35, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[6757]),
        dict(id="mahogany_armchair", name="Mahogany armchair", level=50, xp=280,
             materials=[m(MAHOGANY_PLANK, 2)], objectIds=[6758]),
    ],
    "parlour_bookcase": [
        dict(id="wooden_bookcase", name="Wooden bookcase", level=4, xp=115,
             materials=[m(PLANK, 4), m(NAILS, 4)], objectIds=[6768, 6771]),
        dict(id="oak_bookcase", name="Oak bookcase", level=29, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[6769, 6772]),
        dict(id="mahogany_bookcase", name="Mahogany bookcase", level=40, xp=420,
             materials=[m(MAHOGANY_PLANK, 3)], objectIds=[6770, 6773]),
    ],
    "parlour_curtain": [
        dict(id="torn_curtains", name="Torn curtains", level=2, xp=132,
             materials=[m(PLANK, 3), m(BOLT_OF_CLOTH, 3), m(NAILS, 3)], objectIds=[6774]),
        dict(id="curtains", name="Curtains", level=18, xp=225,
             materials=[m(OAK_PLANK, 3), m(BOLT_OF_CLOTH, 3)], objectIds=[6775]),
        dict(id="opulent_curtains", name="Opulent curtains", level=40, xp=315,
             materials=[m(TEAK_PLANK, 3), m(BOLT_OF_CLOTH, 3)], objectIds=[6776]),
    ],
    "parlour_fireplace": [
        dict(id="clay_fireplace", name="Clay fireplace", level=3, xp=30,
             materials=[m(SOFT_CLAY, 3)], objectIds=[6780, 6781]),
        dict(id="stone_fireplace", name="Stone fireplace", level=33, xp=40,
             materials=[m(LIMESTONE_BRICK, 2)], objectIds=[6782, 6783]),
        dict(id="marble_fireplace", name="Marble fireplace", level=63, xp=500,
             materials=[m(MARBLE_BLOCK, 1)], objectIds=[6784, 6785]),
    ],
    "parlour_rug": [
        dict(id="brown_rug", name="Brown rug", level=2, xp=30,
             materials=[m(BOLT_OF_CLOTH, 2)], objectIds=[6759, 6760, 6761]),
        dict(id="rug", name="Rug", level=13, xp=60,
             materials=[m(BOLT_OF_CLOTH, 4)], objectIds=[6762, 6763, 6764]),
        dict(id="opulent_rug", name="Opulent rug", level=65, xp=360,
             materials=[m(BOLT_OF_CLOTH, 4), m(GOLD_LEAF, 1)], objectIds=[6765, 6766, 6767]),
    ],

    # --- Garden ------------------------------------------------------------
    "garden_big_plant_1": [
        dict(id="fern", name="Fern", level=1, xp=31, materials=[m(BAGGED_PLANT_1, 1)],
             objectIds=[5128], note="Needs a filled watering can"),
        dict(id="bush", name="Bush", level=6, xp=70, materials=[m(BAGGED_PLANT_2, 1)],
             objectIds=[5129], note="Needs a filled watering can"),
        dict(id="tall_plant", name="Tall plant", level=12, xp=100, materials=[m(BAGGED_PLANT_3, 1)],
             objectIds=[5130], note="Needs a filled watering can"),
    ],
    "garden_big_plant_2": [
        dict(id="short_plant", name="Short plant", level=1, xp=31, materials=[m(BAGGED_PLANT_1, 1)],
             objectIds=[5131], note="Needs a filled watering can"),
        dict(id="large_leaf_bush", name="Large leaf bush", level=6, xp=70, materials=[m(BAGGED_PLANT_2, 1)],
             objectIds=[5132], note="Needs a filled watering can"),
        dict(id="huge_plant", name="Huge plant", level=12, xp=100, materials=[m(BAGGED_PLANT_3, 1)],
             objectIds=[5133], note="Needs a filled watering can"),
    ],
    "garden_small_plant_1": [
        dict(id="plant", name="Plant", level=1, xp=31, materials=[m(BAGGED_PLANT_1, 1)],
             objectIds=[5134], note="Needs a filled watering can"),
        dict(id="small_fern", name="Small fern", level=6, xp=70, materials=[m(BAGGED_PLANT_2, 1)],
             objectIds=[5135], note="Needs a filled watering can"),
        dict(id="fern_small", name="Fern", level=12, xp=100, materials=[m(BAGGED_PLANT_3, 1)],
             objectIds=[5136], note="Needs a filled watering can"),
    ],
    "garden_small_plant_2": [
        dict(id="dock_leaf", name="Dock leaf", level=1, xp=31, materials=[m(BAGGED_PLANT_1, 1)],
             objectIds=[5137], note="Needs a filled watering can"),
        dict(id="thistle", name="Thistle", level=6, xp=70, materials=[m(BAGGED_PLANT_2, 1)],
             objectIds=[5138], note="Needs a filled watering can"),
        dict(id="reeds", name="Reeds", level=12, xp=100, materials=[m(BAGGED_PLANT_3, 1)],
             objectIds=[5139], note="Needs a filled watering can"),
    ],
    "garden_tree": [
        dict(id="tree", name="Tree", level=5, xp=31, materials=[m(BAGGED_DEAD_TREE, 1)],
             note="Needs a filled watering can. The crystal saw boost does not work here"),
        dict(id="nice_tree", name="Nice tree", level=10, xp=44, materials=[m(BAGGED_NICE_TREE, 1)]),
        dict(id="oak_tree", name="Oak tree", level=15, xp=70, materials=[m(BAGGED_OAK_TREE, 1)]),
        dict(id="willow_tree", name="Willow tree", level=30, xp=100, materials=[m(BAGGED_WILLOW_TREE, 1)]),
        dict(id="maple_tree", name="Maple tree", level=45, xp=122, materials=[m(BAGGED_MAPLE_TREE, 1)]),
        dict(id="yew_tree", name="Yew tree", level=60, xp=141, materials=[m(BAGGED_YEW_TREE, 1)]),
        dict(id="magic_tree", name="Magic tree", level=75, xp=223, materials=[m(BAGGED_MAGIC_TREE, 1)]),
    ],
    "garden_centrepiece": [
        dict(id="exit_portal", name="Exit portal", level=1, xp=100, materials=[m(IRON_BAR, 10)],
             note="Every house needs one exit portal, in a garden or formal garden"),
        dict(id="decorative_rock", name="Decorative rock", level=5, xp=100, materials=[m(LIMESTONE_BRICK, 5)]),
        dict(id="pond", name="Pond", level=10, xp=100, materials=[m(SOFT_CLAY, 10)]),
        dict(id="imp_statue", name="Imp statue", level=15, xp=150,
             materials=[m(LIMESTONE_BRICK, 5), m(SOFT_CLAY, 5)]),
        dict(id="dungeon_entrance", name="Dungeon entrance", level=70, xp=500, materials=[m(MARBLE_BLOCK, 1)],
             note="Needed to reach the dungeon floor"),
    ],
    "garden_tip_jar": [
        dict(id="tip_jar", name="Tip jar", level=40, xp=651,
             materials=[m(MAHOGANY_PLANK, 2), m(MOLTEN_GLASS, 1), m(GOLD_LEAF, 1), m(PLATINUM_TOKEN, 5)],
             objectIds=[29146]),
    ],

    # --- Kitchen -----------------------------------------------------------
    "kitchen_stove": [
        dict(id="firepit", name="Firepit", level=5, xp=40, materials=[m(STEEL_BAR, 1), m(SOFT_CLAY, 2)],
             objectIds=[13528]),
        dict(id="firepit_hook", name="Firepit with hook", level=11, xp=60,
             materials=[m(STEEL_BAR, 2), m(SOFT_CLAY, 2)], objectIds=[13529, 13530]),
        dict(id="firepit_pot", name="Firepit with pot", level=17, xp=80,
             materials=[m(STEEL_BAR, 3), m(SOFT_CLAY, 2)], objectIds=[13531, 13532]),
        dict(id="small_oven", name="Small oven", level=24, xp=80, materials=[m(STEEL_BAR, 4)],
             objectIds=[13533, 13534, 13535]),
        dict(id="large_oven", name="Large oven", level=29, xp=100, materials=[m(STEEL_BAR, 5)],
             objectIds=[13536, 13537, 13538]),
        dict(id="steel_range", name="Steel range", level=34, xp=120, materials=[m(STEEL_BAR, 6)],
             objectIds=[13539, 13540, 13541]),
        dict(id="fancy_range", name="Fancy range", level=42, xp=160, materials=[m(STEEL_BAR, 8)],
             objectIds=[13542, 13543, 13544]),
    ],
    "kitchen_shelf": [
        dict(id="wooden_shelves_1", name="Wooden shelves 1", level=6, xp=87,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[13545, 13552]),
        dict(id="wooden_shelves_2", name="Wooden shelves 2", level=12, xp=147,
             materials=[m(PLANK, 3), m(NAILS, 3), m(SOFT_CLAY, 6)], objectIds=[13546, 13553]),
        dict(id="wooden_shelves_3", name="Wooden shelves 3", level=23, xp=147,
             materials=[m(PLANK, 3), m(NAILS, 3), m(SOFT_CLAY, 6)], objectIds=[13547, 13554],
             note="Better tea boost than oak shelves 1, so worth keeping until oak shelves 2"),
        dict(id="oak_shelves_1", name="Oak shelves 1", level=34, xp=240,
             materials=[m(OAK_PLANK, 3), m(SOFT_CLAY, 6)], objectIds=[13548, 13555]),
        dict(id="oak_shelves_2", name="Oak shelves 2", level=45, xp=240,
             materials=[m(OAK_PLANK, 3), m(SOFT_CLAY, 6)], objectIds=[13549, 13556]),
        dict(id="teak_shelves_1", name="Teak shelves 1", level=56, xp=330,
             materials=[m(TEAK_PLANK, 3), m(SOFT_CLAY, 6)], objectIds=[13550, 13557]),
        dict(id="teak_shelves_2", name="Teak shelves 2", level=67, xp=930,
             materials=[m(TEAK_PLANK, 3), m(SOFT_CLAY, 6), m(GOLD_LEAF, 2)], objectIds=[13551, 13558]),
    ],
    "kitchen_larder": [
        dict(id="wooden_larder", name="Wooden larder", level=9, xp=228,
             materials=[m(PLANK, 8), m(NAILS, 8)], objectIds=[13565]),
        dict(id="oak_larder", name="Oak larder", level=33, xp=480,
             materials=[m(OAK_PLANK, 8)], objectIds=[13566]),
        dict(id="teak_larder", name="Teak larder", level=43, xp=750,
             materials=[m(TEAK_PLANK, 8), m(BOLT_OF_CLOTH, 2)], objectIds=[13567]),
    ],
    "kitchen_sink": [
        dict(id="pump_and_drain", name="Pump and drain", level=7, xp=100, materials=[m(STEEL_BAR, 5)],
             objectIds=[13559, 13560]),
        dict(id="pump_and_tub", name="Pump and tub", level=27, xp=200, materials=[m(STEEL_BAR, 10)],
             objectIds=[13561, 13562]),
        dict(id="sink", name="Sink", level=47, xp=300, materials=[m(STEEL_BAR, 15)],
             objectIds=[13563, 13564]),
        dict(id="gold_sink", name="Gold sink", level=47, xp=11144,
             materials=[m(CONDENSED_GOLD, 10), m(MAHOGANY_PLANK, 5), m(GOLD_LEAF, 5)],
             objectIds=[26458, 42852]),
    ],
    "kitchen_barrel": [
        dict(id="beer_barrel", name="Beer barrel", level=7, xp=87,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[13568]),
        dict(id="cider_barrel", name="Cider barrel", level=12, xp=91,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[13569],
             note="Also needs 8 cider"),
        dict(id="asgarnian_ale", name="Asgarnian ale", level=18, xp=184,
             materials=[m(OAK_PLANK, 3)], objectIds=[13570], note="Also needs 8 Asgarnian ale"),
        dict(id="greenmans_ale", name="Greenman's ale", level=26, xp=184,
             materials=[m(OAK_PLANK, 3)], objectIds=[13571], note="Also needs 8 Greenman's ale"),
        dict(id="dragon_bitter", name="Dragon bitter", level=36, xp=224,
             materials=[m(OAK_PLANK, 3), m(STEEL_BAR, 2)], objectIds=[13572],
             note="Also needs 8 Dragon bitter"),
        dict(id="chefs_delight", name="Chef's delight", level=48, xp=224,
             materials=[m(OAK_PLANK, 3), m(STEEL_BAR, 2)], objectIds=[13573],
             note="Also needs 8 Chef's delight"),
    ],
    "kitchen_cat_basket": [
        dict(id="cat_blanket", name="Cat blanket", level=5, xp=15, materials=[m(BOLT_OF_CLOTH, 1)]),
        dict(id="cat_basket", name="Cat basket", level=19, xp=58, materials=[m(PLANK, 2), m(NAILS, 2)]),
        dict(id="cushioned_basket", name="Cushioned basket", level=33, xp=58,
             materials=[m(PLANK, 2), m(NAILS, 2), m(WOOL, 2)]),
    ],
    "kitchen_table": [
        dict(id="kitchen_table", name="Kitchen table", level=12, xp=87,
             materials=[m(PLANK, 3), m(NAILS, 3)], objectIds=[13577]),
        dict(id="oak_kitchen_table", name="Oak kitchen table", level=32, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[13578]),
        dict(id="teak_kitchen_table", name="Teak kitchen table", level=52, xp=270,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13579]),
    ],
    "kitchen_spice_rack": [
        dict(id="spice_rack", name="Spice rack", level=60, xp=374,
             materials=[m(TEAK_PLANK, 3), m(SOFT_CLAY, 6)], objectIds=[37621],
             note="Also needs 4 doses each of brown, orange, red and yellow spice"),
    ],

    # --- Dining room -------------------------------------------------------
    "dining_table": [
        dict(id="wood_dining_table", name="Wood dining table", level=10, xp=115,
             materials=[m(PLANK, 4), m(NAILS, 4)], objectIds=[13293]),
        dict(id="oak_dining_table", name="Oak dining table", level=22, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[13294]),
        dict(id="carved_oak_table", name="Carved oak table", level=31, xp=360,
             materials=[m(OAK_PLANK, 6)], objectIds=[13295]),
        dict(id="teak_table", name="Teak table", level=38, xp=360,
             materials=[m(TEAK_PLANK, 4)], objectIds=[13296]),
        dict(id="carved_teak_table", name="Carved teak table", level=45, xp=600,
             materials=[m(TEAK_PLANK, 6), m(BOLT_OF_CLOTH, 4)], objectIds=[13297]),
        dict(id="mahogany_table", name="Mahogany table", level=52, xp=840,
             materials=[m(MAHOGANY_PLANK, 6)], objectIds=[13298]),
        dict(id="opulent_table", name="Opulent table", level=72, xp=3100,
             materials=[m(MAHOGANY_PLANK, 6), m(BOLT_OF_CLOTH, 4), m(GOLD_LEAF, 4), m(MARBLE_BLOCK, 2)],
             objectIds=[13299]),
    ],
    "dining_seating": [
        dict(id="wooden_bench", name="Wooden bench", level=10, xp=115,
             materials=[m(PLANK, 4), m(NAILS, 4)], objectIds=[13300, 26210]),
        dict(id="oak_bench", name="Oak bench", level=22, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[13301, 26211]),
        dict(id="carved_oak_bench", name="Carved oak bench", level=31, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[13302, 26212]),
        dict(id="teak_dining_bench", name="Teak dining bench", level=38, xp=360,
             materials=[m(TEAK_PLANK, 4)], objectIds=[13303, 26213]),
        dict(id="carved_teak_bench", name="Carved teak bench", level=44, xp=360,
             materials=[m(TEAK_PLANK, 4)], objectIds=[13304, 26214]),
        dict(id="mahogany_bench", name="Mahogany bench", level=52, xp=560,
             materials=[m(MAHOGANY_PLANK, 4)], objectIds=[13305, 26215]),
        dict(id="gilded_bench", name="Gilded bench", level=61, xp=1760,
             materials=[m(MAHOGANY_PLANK, 4), m(GOLD_LEAF, 4)], objectIds=[13306, 26216]),
    ],
    "dining_bell_pull": [
        dict(id="rope_bell_pull", name="Rope bell-pull", level=26, xp=64,
             materials=[m(OAK_PLANK, 1)], objectIds=[13307], note="Also needs a rope"),
        dict(id="bell_pull", name="Bell-pull", level=37, xp=120,
             materials=[m(TEAK_PLANK, 1), m(BOLT_OF_CLOTH, 2)], objectIds=[13308]),
        dict(id="posh_bell_pull", name="Posh bell-pull", level=60, xp=420,
             materials=[m(TEAK_PLANK, 1), m(BOLT_OF_CLOTH, 2), m(GOLD_LEAF, 1)], objectIds=[13309]),
    ],
    "dining_decoration": [
        dict(id="oak_wall_decoration", name="Oak wall decoration", level=16, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=list(range(13798, 13814)),
             note="Needs a family crest from Sir Renitee in White Knights' Castle"),
        dict(id="teak_wall_decoration", name="Teak wall decoration", level=36, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=list(range(13814, 13830)),
             note="Needs a family crest from Sir Renitee in White Knights' Castle"),
        dict(id="gilded_decoration", name="Gilded decoration", level=56, xp=1020,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 2)], objectIds=list(range(13782, 13798)),
             note="Needs a family crest from Sir Renitee in White Knights' Castle"),
    ],

    # --- Bedroom -----------------------------------------------------------
    "bedroom_bed": [
        dict(id="wooden_bed", name="Wooden bed", level=20, xp=117,
             materials=[m(PLANK, 3), m(NAILS, 3), m(BOLT_OF_CLOTH, 2)], objectIds=[13148]),
        dict(id="oak_bed", name="Oak bed", level=30, xp=210,
             materials=[m(OAK_PLANK, 3), m(BOLT_OF_CLOTH, 2)], objectIds=[13149]),
        dict(id="large_oak_bed", name="Large oak bed", level=34, xp=330,
             materials=[m(OAK_PLANK, 5), m(BOLT_OF_CLOTH, 2)], objectIds=[13150]),
        dict(id="teak_bed", name="Teak bed", level=40, xp=300,
             materials=[m(TEAK_PLANK, 3), m(BOLT_OF_CLOTH, 2)], objectIds=[13151]),
        dict(id="large_teak_bed", name="Large teak bed", level=45, xp=480,
             materials=[m(TEAK_PLANK, 5), m(BOLT_OF_CLOTH, 2)], objectIds=[13152]),
        dict(id="four_poster", name="4-poster", level=53, xp=450,
             materials=[m(MAHOGANY_PLANK, 3), m(BOLT_OF_CLOTH, 2)], objectIds=[13153]),
        dict(id="gilded_four_poster", name="Gilded 4-poster", level=60, xp=1330,
             materials=[m(MAHOGANY_PLANK, 5), m(BOLT_OF_CLOTH, 2), m(GOLD_LEAF, 2)], objectIds=[13154]),
    ],
    "bedroom_wardrobe": [
        dict(id="shoe_box", name="Shoe box", level=20, xp=58,
             materials=[m(PLANK, 2), m(NAILS, 2)], objectIds=[13155]),
        dict(id="oak_drawers", name="Oak drawers", level=27, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13156]),
        dict(id="oak_wardrobe", name="Oak wardrobe", level=39, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[13157]),
        dict(id="teak_drawers", name="Teak drawers", level=51, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13158]),
        dict(id="teak_wardrobe", name="Teak wardrobe", level=63, xp=270,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13159]),
        dict(id="mahogany_wardrobe", name="Mahogany wardrobe", level=75, xp=420,
             materials=[m(MAHOGANY_PLANK, 3)], objectIds=[13160]),
        dict(id="gilded_wardrobe", name="Gilded wardrobe", level=87, xp=720,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 1)], objectIds=[13161]),
    ],
    "bedroom_dresser": [
        dict(id="shaving_stand", name="Shaving stand", level=21, xp=30,
             materials=[m(PLANK, 1), m(NAILS, 1), m(MOLTEN_GLASS, 1)]),
        dict(id="oak_shaving_stand", name="Oak shaving stand", level=29, xp=61,
             materials=[m(OAK_PLANK, 1), m(MOLTEN_GLASS, 1)]),
        dict(id="oak_dresser", name="Oak dresser", level=37, xp=121,
             materials=[m(OAK_PLANK, 2), m(MOLTEN_GLASS, 1)]),
        dict(id="teak_dresser", name="Teak dresser", level=46, xp=181,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 1)]),
        dict(id="fancy_teak_dresser", name="Fancy teak dresser", level=56, xp=182,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 2)]),
        dict(id="mahogany_dresser", name="Mahogany dresser", level=64, xp=281,
             materials=[m(MAHOGANY_PLANK, 2), m(MOLTEN_GLASS, 1)]),
        dict(id="gilded_dresser", name="Gilded dresser", level=74, xp=582,
             materials=[m(MAHOGANY_PLANK, 2), m(MOLTEN_GLASS, 2), m(GOLD_LEAF, 1)]),
    ],
    "bedroom_corner": [
        dict(id="oak_clock", name="Oak clock", level=25, xp=142,
             materials=[m(OAK_PLANK, 2)], objectIds=[13169], note="Also needs clockwork"),
        dict(id="teak_clock", name="Teak clock", level=55, xp=202,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13170], note="Also needs clockwork"),
        dict(id="servants_money_bag", name="Servant's money bag", level=58, xp=595,
             materials=[m(MAHOGANY_PLANK, 2), m(BOLT_OF_CLOTH, 1), m(GOLD_LEAF, 1)],
             note="Pays your servant automatically"),
        dict(id="gilded_clock", name="Gilded clock", level=85, xp=602,
             materials=[m(MAHOGANY_PLANK, 2), m(GOLD_LEAF, 1)], objectIds=[13171],
             note="Also needs clockwork"),
    ],

    # --- Skill hall --------------------------------------------------------
    "hall_stairs": [
        dict(id="rug_stairs_brown", name="Rug", level=13, xp=60, materials=[m(BOLT_OF_CLOTH, 4)]),
        dict(id="oak_staircase", name="Oak staircase", level=27, xp=680,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 4)]),
        dict(id="teak_staircase", name="Teak staircase", level=48, xp=980,
             materials=[m(TEAK_PLANK, 10), m(STEEL_BAR, 4)]),
        dict(id="opulent_rug_stairs", name="Opulent rug", level=65, xp=360,
             materials=[m(BOLT_OF_CLOTH, 4), m(GOLD_LEAF, 1)]),
        dict(id="limestone_spiral", name="Limestone spiral staircase", level=67, xp=1040,
             materials=[m(TEAK_PLANK, 10), m(LIMESTONE_BRICK, 7)]),
        dict(id="marble_staircase", name="Marble staircase", level=82, xp=3200,
             materials=[m(MAHOGANY_PLANK, 5), m(MARBLE_BLOCK, 5)]),
        dict(id="marble_spiral", name="Marble spiral", level=97, xp=4400,
             materials=[m(TEAK_PLANK, 10), m(MARBLE_BLOCK, 7)]),
    ],
    "hall_head_trophy": [
        dict(id="teak_head_display", name="Teak display", level=38, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[56110]),
        dict(id="mahogany_head_display", name="Mahogany display", level=58, xp=280,
             materials=[m(MAHOGANY_PLANK, 2)], objectIds=[56111]),
        dict(id="gilded_head_display", name="Gilded display", level=78, xp=600,
             materials=[m(MAHOGANY_PLANK, 2), m(GOLD_LEAF, 2)], objectIds=[56112],
             note="Planks not needed when upgrading from the mahogany display"),
    ],
    "hall_fishing_trophy": [
        dict(id="oak_fish_display", name="Oak display", level=36, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[56130]),
        dict(id="teak_fish_display", name="Teak display", level=56, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[56131]),
        dict(id="mahogany_fish_display", name="Mahogany display", level=76, xp=280,
             materials=[m(MAHOGANY_PLANK, 2)], objectIds=[56132]),
    ],
    "hall_armour": [
        dict(id="cw_armour_1", name="Castle Wars armour 1", level=28, xp=135,
             materials=[m(OAK_PLANK, 2)], objectIds=[13494],
             note="Also needs a decorative helm, armour and shield"),
        dict(id="cw_armour_2", name="Castle Wars armour 2", level=28, xp=150,
             materials=[m(OAK_PLANK, 2)], objectIds=[13495],
             note="Also needs a decorative helm, armour and shield"),
        dict(id="cw_armour_3", name="Castle Wars armour 3", level=28, xp=165,
             materials=[m(OAK_PLANK, 2)], objectIds=[13496],
             note="Also needs a decorative helm, armour and shield"),
        dict(id="mithril_armour", name="Mithril armour", level=28, xp=135,
             materials=[m(OAK_PLANK, 2)], objectIds=[13491],
             note="Also needs a mithril full helm, platebody and plateskirt. Not trimmed"),
        dict(id="adamantite_armour", name="Adamantite armour", level=28, xp=150,
             materials=[m(OAK_PLANK, 2)], objectIds=[13492],
             note="Also needs an adamant full helm, platebody and plateskirt. Not trimmed"),
        dict(id="runite_armour", name="Runite armour", level=28, xp=165,
             materials=[m(OAK_PLANK, 2)], objectIds=[13493],
             note="Also needs a rune full helm, platebody and plateskirt. Not trimmed"),
    ],
    "hall_rune_case": [
        dict(id="rune_case_1", name="Rune case 1", level=41, xp=190,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 2)],
             note="Also needs an air, earth, fire and water rune"),
        dict(id="rune_case_2", name="Rune case 2", level=41, xp=212,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 2)],
             note="Also needs a body, chaos, cosmic and nature rune"),
        dict(id="rune_case_3", name="Rune case 3", level=41, xp=247,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 2)],
             note="Also needs a blood, death, law and soul rune"),
    ],
}

# ---------------------------------------------------------------------------
# Rooms. `objects` on a hotspot are the empty build hotspot object ids from the
# cache; `family` names the entry in FURNITURE holding what can go there.
# `planes`: 0 dungeon, 1 ground floor, 2 first floor.
# ---------------------------------------------------------------------------

GROUND_AND_UP = [1, 2]

ROOMS = [
    dict(
        id="garden", name="Garden", level=1, cost=1000, planes=[1], colour="#4C7A3F",
        note="Every house needs at least one garden or formal garden, for the exit portal",
        hotspots=[
            dict(id="centrepiece", name="Centrepiece space", objects=[15361], family="garden_centrepiece"),
            dict(id="big_tree", name="Big tree space", objects=[15362], family="garden_tree"),
            dict(id="tree", name="Tree space", objects=[15363], family="garden_tree"),
            dict(id="big_plant_1", name="Big plant space 1", objects=[15364], family="garden_big_plant_1"),
            dict(id="big_plant_2", name="Big plant space 2", objects=[15365], family="garden_big_plant_2"),
            dict(id="small_plant_1", name="Small plant space 1", objects=[15366], family="garden_small_plant_1"),
            dict(id="small_plant_2", name="Small plant space 2", objects=[15367], family="garden_small_plant_2"),
            dict(id="tip_jar", name="Tip jar space", objects=[29119], family="garden_tip_jar"),
        ],
    ),
    dict(
        id="parlour", name="Parlour", level=1, cost=1000, planes=GROUND_AND_UP, colour="#8B6F47",
        hotspots=[
            dict(id="chair_1", name="Chair space 1", objects=[4515], family="parlour_chair"),
            dict(id="chair_2", name="Chair space 2", objects=[4516], family="parlour_chair"),
            dict(id="chair_3", name="Chair space 3", objects=[4517], family="parlour_chair"),
            dict(id="rug", name="Rug space", objects=[4518, 4519, 4520], family="parlour_rug"),
            dict(id="bookcase", name="Bookcase space", objects=[4521, 4522], family="parlour_bookcase"),
            dict(id="fireplace", name="Fireplace space", objects=[4523], family="parlour_fireplace"),
            dict(id="curtain", name="Curtain space", objects=[4524], family="parlour_curtain"),
        ],
    ),
    dict(
        id="kitchen", name="Kitchen", level=5, cost=5000, planes=GROUND_AND_UP, colour="#B07A3C",
        note="Two non-parallel door spaces, which makes it a good corner room",
        hotspots=[
            dict(id="stove", name="Stove space", objects=[15398], family="kitchen_stove"),
            dict(id="shelf", name="Shelf space", objects=[15399, 15400], family="kitchen_shelf"),
            dict(id="barrel", name="Barrel space", objects=[15401], family="kitchen_barrel"),
            dict(id="cat_basket", name="Cat basket space", objects=[15402], family="kitchen_cat_basket"),
            dict(id="larder", name="Larder space", objects=[15403], family="kitchen_larder"),
            dict(id="sink", name="Sink space", objects=[15404], family="kitchen_sink"),
            dict(id="table", name="Table space", objects=[15405], family="kitchen_table"),
            dict(id="spice_rack", name="Spice rack space", objects=[37620], family="kitchen_spice_rack"),
        ],
    ),
    dict(
        id="dining_room", name="Dining room", level=10, cost=5000, planes=GROUND_AND_UP, colour="#9C5B3C",
        note="A servant serves food here. The bell-pull summons your servant instantly",
        hotspots=[
            dict(id="table", name="Table space", objects=[15298], family="dining_table"),
            dict(id="seating_1", name="Seating space 1", objects=[15299], family="dining_seating"),
            dict(id="seating_2", name="Seating space 2", objects=[15300], family="dining_seating"),
            dict(id="fireplace", name="Fireplace space", objects=[15301], family="parlour_fireplace"),
            dict(id="curtain", name="Curtain space", objects=[15302], family="parlour_curtain"),
            dict(id="decoration", name="Decoration space", objects=[15303], family="dining_decoration"),
            dict(id="bell_pull", name="Bell pull space", objects=[15304], family="dining_bell_pull"),
        ],
    ),
    dict(
        id="bedroom", name="Bedroom", level=20, cost=10000, planes=GROUND_AND_UP, colour="#6B5B95",
        note="Two bedrooms with beds are needed before you can hire a servant. Two non-parallel doors, so a good corner room",
        hotspots=[
            dict(id="bed", name="Bed space", objects=[15260], family="bedroom_bed"),
            dict(id="wardrobe", name="Wardrobe space", objects=[15261], family="bedroom_wardrobe"),
            dict(id="dresser", name="Dresser space", objects=[15262], family="bedroom_dresser"),
            dict(id="curtain", name="Curtain space", objects=[15263], family="parlour_curtain"),
            dict(id="rug", name="Rug space", objects=[15264, 15265, 15266], family="parlour_rug"),
            dict(id="fireplace", name="Fireplace space", objects=[15267], family="parlour_fireplace"),
            dict(id="corner", name="Corner space", objects=[15268], family="bedroom_corner"),
        ],
    ),
    dict(
        id="skill_hall", name="Hall (skill trophies)", level=25, cost=15000, planes=GROUND_AND_UP,
        colour="#3E6B8A",
        note="Also called the skill hall. A staircase here links floors, and can lead down to a dungeon stairs room",
        hotspots=[
            dict(id="stairs", name="Stair space", objects=[15377, 15378, 15379, 15380, 15381],
                 family="hall_stairs"),
            dict(id="head_trophy", name="Head trophy space", objects=[15382], family="hall_head_trophy"),
            dict(id="fishing_trophy", name="Fishing trophy space", objects=[15383],
                 family="hall_fishing_trophy"),
            dict(id="armour_1", name="Armour space 1", objects=[15384], family="hall_armour"),
            dict(id="armour_2", name="Armour space 2", objects=[15385], family="hall_armour"),
            dict(id="rune_case", name="Rune case space", objects=[15386], family="hall_rune_case"),
        ],
    ),
]


def build():
    rooms = []
    for room in ROOMS:
        hotspots = []
        for hotspot in room["hotspots"]:
            options = FURNITURE.get(hotspot["family"])
            if options is None:
                raise SystemExit(
                    "room %s hotspot %s references unknown furniture family %s"
                    % (room["id"], hotspot["id"], hotspot["family"])
                )
            hotspots.append(dict(
                id=hotspot["id"],
                name=hotspot["name"],
                objectIds=hotspot["objects"],
                options=[_clean(option) for option in options],
            ))

        entry = dict(
            id=room["id"],
            name=room["name"],
            level=room["level"],
            cost=room["cost"],
            planes=room["planes"],
            colour=room["colour"],
            hotspots=hotspots,
        )
        if room.get("doors"):
            entry["doors"] = room["doors"]
        if room.get("note"):
            entry["note"] = room["note"]
        rooms.append(entry)

    data = dict(format=FORMAT, styles=STYLES, rooms=rooms, items=ITEM_INFO)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=1, ensure_ascii=False)
        handle.write("\n")

    hotspot_count = sum(len(r["hotspots"]) for r in rooms)
    option_count = sum(len(h["options"]) for r in rooms for h in r["hotspots"])
    print("wrote %s" % OUT)
    print("  %d rooms, %d hotspots, %d furniture options, %d items"
          % (len(rooms), hotspot_count, option_count, len(ITEM_INFO)))
    _check_ids(rooms)


def _clean(option):
    entry = dict(
        id=option["id"],
        name=option["name"],
        level=option["level"],
        xp=option["xp"],
        materials=option.get("materials", []),
    )
    if option.get("objectIds"):
        entry["objectIds"] = option["objectIds"]
    if option.get("note"):
        entry["note"] = option["note"]
    return entry


def _check_ids(rooms):
    """An object id must not mean two different hotspots in the same room."""
    problems = 0
    for room in rooms:
        seen = {}
        for hotspot in room["hotspots"]:
            for object_id in hotspot["objectIds"]:
                if object_id in seen:
                    print("  WARNING: object %d is on both %s and %s in %s"
                          % (object_id, seen[object_id], hotspot["id"], room["id"]))
                    problems += 1
                seen[object_id] = hotspot["id"]
    if not problems:
        print("  object id check passed")


if __name__ == "__main__":
    build()
