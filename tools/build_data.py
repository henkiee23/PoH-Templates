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
UNPOWERED_ORB = 567
ROPE = 954
CLOCKWORK = 8792
CANDLE = 36
GOLD_BAR = 2357
PAPYRUS = 970
BUCKET_OF_SAND = 1783
BUCKET_OF_MILK = 1927
BUCKET_OF_WATER = 1929
COMPOST = 6032
SUPERCOMPOST = 6034
RED_DYE = 1763
BLUE_DYE = 1767
PINK_DYE = 6955
SKULL = 964
BONES = 526
GRANITE_5KG = 6983
MUSHROOM = 6004
REDWOOD_LOGS = 19669
ONYX = 6573
LIT_CANDLE = 33
LIT_TORCH = 594

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
    dict(itemId=UNPOWERED_ORB, name="Unpowered orb", sources=[
        "Blow molten glass with a glassblowing pipe (46 Crafting)",
        "Buy from the Magic Guild store in Yanille",
    ]),
    dict(itemId=ROPE, name="Rope", sources=[
        "Spin 4 balls of wool on a spinning wheel (30 Crafting)",
        "Buy from most general stores",
    ]),
    dict(itemId=CLOCKWORK, name="Clockwork", sources=[
        "Make it on a crafting table 2 or better in your own workshop, from a steel bar",
    ]),
    dict(itemId=CANDLE, name="Candle", sources=[
        "Buy from the candle shop in Catherby",
        "Make from wax and a candle mould",
    ]),
    dict(itemId=GOLD_BAR, name="Gold bar", sources=["Smelt gold ore (40 Smithing)"]),
    dict(itemId=PAPYRUS, name="Papyrus", sources=["Buy from most general stores, or a Trader Crewmember"]),
    dict(itemId=BUCKET_OF_SAND, name="Bucket of sand", sources=[
        "Fill a bucket at a sand pit, e.g. Yanille or the Bandit Camp",
        "Buy from the Bert delivery in Yanille after The Hand in the Sand",
    ]),
    dict(itemId=BUCKET_OF_MILK, name="Bucket of milk", sources=["Milk a dairy cow with an empty bucket"]),
    dict(itemId=BUCKET_OF_WATER, name="Bucket of water", sources=["Fill a bucket at any water source"]),
    dict(itemId=COMPOST, name="Compost", sources=["Fill a compost bin with 15 vegetables or weeds"]),
    dict(itemId=SUPERCOMPOST, name="Supercompost", sources=[
        "Fill a compost bin with 15 high-quality produce, e.g. pineapples or watermelons",
    ]),
    dict(itemId=RED_DYE, name="Red dye", sources=["Aggie in Draynor Village, from 3 redberries and 5 coins"]),
    dict(itemId=BLUE_DYE, name="Blue dye", sources=["Aggie in Draynor Village, from 2 woad leaves and 5 coins"]),
    dict(itemId=PINK_DYE, name="Pink dye", sources=["Aggie in Draynor Village, from red dye and a bucket of milk"]),
    dict(itemId=SKULL, name="Skull", sources=["Drop from skeletons, or spawns in the Wilderness and Varrock sewers"]),
    dict(itemId=BONES, name="Bones", sources=["Drop from most low-level monsters"]),
    dict(itemId=GRANITE_5KG, name="Granite (5kg)", sources=["Mine granite in the Bandit Camp quarry (45 Mining)"]),
    dict(itemId=MUSHROOM, name="Mushroom", sources=["Pick bittercap mushrooms in Mort Myre or Canifis"]),
    dict(itemId=REDWOOD_LOGS, name="Redwood logs", sources=["Chop a redwood tree in the Woodcutting Guild (90 Woodcutting)"]),
    dict(itemId=ONYX, name="Onyx", sources=[
        "Buy from the Tzhaar gem store in Mor Ul Rek",
        "Rare drop from Zulrah and the Gauntlet",
    ]),
    dict(itemId=LIT_CANDLE, name="Lit candle", sources=["Light a candle with a tinderbox"]),
    dict(itemId=LIT_TORCH, name="Lit torch", sources=["Light a torch with a tinderbox"]),
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


# The chapel's alignment is chosen by its icon and restyles the altar and statues; it does not
# change what they cost, so each tier simply lists every variant's object id.
ALIGN = ("The chapel's alignment (Saradomin, Zamorak, Guthix, Bob or Gnome child) is set by the "
         "icon and changes how this looks. It costs the same either way")


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

    # --- Workshop ----------------------------------------------------------
    # The tool store, crafting table and workbench upgrade in place: a higher tier can only be
    # built on top of the one below it. Materials here are therefore CUMULATIVE, counting every
    # tier you must pass through, so the shopping list totals what the whole climb costs.
    "workshop_workbench": [
        dict(id="wooden_workbench", name="Wooden workbench", level=17, xp=143,
             materials=[m(PLANK, 5), m(NAILS, 5)], objectIds=[6791]),
        dict(id="oak_workbench", name="Oak workbench", level=32, xp=300,
             materials=[m(OAK_PLANK, 5)], objectIds=[6792]),
        dict(id="steel_framed_workbench", name="Steel framed workbench", level=46, xp=440,
             materials=[m(OAK_PLANK, 6), m(STEEL_BAR, 4)], objectIds=[6793]),
        dict(id="bench_with_vice", name="Bench with vice", level=62, xp=140,
             materials=[m(OAK_PLANK, 8), m(STEEL_BAR, 5)], objectIds=[6794],
             note="Built on top of the steel framed workbench; materials include that tier"),
        dict(id="bench_with_lathe", name="Bench with lathe", level=77, xp=140,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 6)], objectIds=[6795],
             note="Built on top of the bench with vice; materials include every tier below"),
    ],
    "workshop_clockmaking": [
        dict(id="crafting_table_1", name="Crafting table 1", level=16, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[6796]),
        dict(id="crafting_table_2", name="Crafting table 2", level=25, xp=1,
             materials=[m(OAK_PLANK, 4), m(MOLTEN_GLASS, 1)], objectIds=[6797],
             note="Upgrades table 1; materials include that tier"),
        dict(id="crafting_table_3", name="Crafting table 3", level=34, xp=2,
             materials=[m(OAK_PLANK, 4), m(MOLTEN_GLASS, 3)], objectIds=[6798],
             note="Upgrades table 2; materials include every tier below"),
        dict(id="crafting_table_4", name="Crafting table 4", level=42, xp=120,
             materials=[m(OAK_PLANK, 6), m(MOLTEN_GLASS, 3)], objectIds=[6799],
             note="Upgrades table 3; materials include every tier below"),
    ],
    "workshop_tool": [
        dict(id="tool_store_1", name="Tool store 1", level=15, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[6786]),
        dict(id="tool_store_2", name="Tool store 2", level=25, xp=120,
             materials=[m(OAK_PLANK, 4)], objectIds=[6787], note="Materials include every tier below"),
        dict(id="tool_store_3", name="Tool store 3", level=35, xp=120,
             materials=[m(OAK_PLANK, 6)], objectIds=[6788], note="Materials include every tier below"),
        dict(id="tool_store_4", name="Tool store 4", level=44, xp=120,
             materials=[m(OAK_PLANK, 8)], objectIds=[6789], note="Materials include every tier below"),
        dict(id="tool_store_5", name="Tool store 5", level=55, xp=120,
             materials=[m(OAK_PLANK, 10)], objectIds=[6790], note="Materials include every tier below"),
    ],
    "workshop_repair": [
        dict(id="repair_bench", name="Repair bench", level=15, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[6800]),
        dict(id="whetstone", name="Whetstone", level=35, xp=260,
             materials=[m(OAK_PLANK, 4), m(LIMESTONE_BRICK, 1)], objectIds=[6801]),
        dict(id="armour_stand", name="Armour stand", level=55, xp=500,
             materials=[m(OAK_PLANK, 8), m(LIMESTONE_BRICK, 1)], objectIds=[6802]),
    ],
    "workshop_heraldry": [
        dict(id="pluming_stand", name="Pluming stand", level=16, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[6803]),
        dict(id="shield_easel", name="Shield easel", level=41, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[6804]),
        dict(id="banner_easel", name="Banner easel", level=66, xp=510,
             materials=[m(OAK_PLANK, 8), m(BOLT_OF_CLOTH, 2)], objectIds=[6805]),
    ],

    # --- Study -------------------------------------------------------------
    "study_lectern": [
        dict(id="oak_lectern", name="Oak lectern", level=40, xp=60,
             materials=[m(OAK_PLANK, 1)], objectIds=[13642]),
        dict(id="eagle_lectern", name="Eagle lectern", level=47, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13643]),
        dict(id="demon_lectern", name="Demon lectern", level=47, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13644]),
        dict(id="teak_eagle_lectern", name="Teak eagle lectern", level=57, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13645]),
        dict(id="teak_demon_lectern", name="Teak demon lectern", level=57, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13646]),
        dict(id="mahogany_eagle_lectern", name="Mahogany eagle lectern", level=67, xp=580,
             materials=[m(MAHOGANY_PLANK, 2), m(GOLD_LEAF, 1)], objectIds=[13647]),
        dict(id="mahogany_demon_lectern", name="Mahogany demon lectern", level=67, xp=580,
             materials=[m(MAHOGANY_PLANK, 2), m(GOLD_LEAF, 1)], objectIds=[13648]),
        dict(id="marble_lectern", name="Marble lectern", level=77, xp=1800,
             materials=[m(MARBLE_BLOCK, 1), m(MAGIC_STONE, 1), m(GOLD_LEAF, 1)], objectIds=[37349]),
    ],
    "study_globe": [
        dict(id="globe", name="Globe", level=41, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[13649]),
        dict(id="ornamental_globe", name="Ornamental globe", level=50, xp=270,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13650]),
        dict(id="lunar_globe", name="Lunar globe", level=59, xp=570,
             materials=[m(TEAK_PLANK, 3), m(GOLD_LEAF, 1)], objectIds=[13651]),
        dict(id="celestial_globe", name="Celestial globe", level=68, xp=570,
             materials=[m(TEAK_PLANK, 3), m(GOLD_LEAF, 1)], objectIds=[13652]),
        dict(id="armillary_sphere", name="Armillary sphere", level=77, xp=960,
             materials=[m(MAHOGANY_PLANK, 2), m(GOLD_LEAF, 2), m(STEEL_BAR, 4)], objectIds=[13653]),
        dict(id="small_orrery", name="Small orrery", level=86, xp=1320,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 3)], objectIds=[13654]),
        dict(id="large_orrery", name="Large orrery", level=95, xp=1420,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 5)], objectIds=[13655]),
    ],
    "study_crystal_ball": [
        dict(id="crystal_ball", name="Crystal ball", level=42, xp=280,
             materials=[m(TEAK_PLANK, 3), m(UNPOWERED_ORB, 1)], objectIds=[13659]),
        dict(id="elemental_sphere", name="Elemental sphere", level=54, xp=580,
             materials=[m(TEAK_PLANK, 3), m(UNPOWERED_ORB, 1), m(GOLD_LEAF, 1)], objectIds=[13660]),
        dict(id="crystal_of_power", name="Crystal of power", level=66, xp=890,
             materials=[m(MAHOGANY_PLANK, 2), m(UNPOWERED_ORB, 1), m(GOLD_LEAF, 2)], objectIds=[13661]),
    ],
    "study_telescope": [
        dict(id="oak_telescope", name="Oak telescope", level=44, xp=121,
             materials=[m(OAK_PLANK, 2), m(MOLTEN_GLASS, 1)], objectIds=[13656]),
        dict(id="teak_telescope", name="Teak telescope", level=64, xp=181,
             materials=[m(TEAK_PLANK, 2), m(MOLTEN_GLASS, 1)], objectIds=[13657]),
        dict(id="mahogany_telescope", name="Mahogany telescope", level=84, xp=580,
             materials=[m(MAHOGANY_PLANK, 2), m(MOLTEN_GLASS, 1)], objectIds=[13658]),
    ],
    "study_wall_chart": [
        dict(id="stash_chart", name="S.t.a.s.h chart", level=40, xp=16,
             materials=[m(BOLT_OF_CLOTH, 1)], objectIds=[41434],
             note="Also needs a S.t.a.s.h blueprint"),
        dict(id="alchemical_chart", name="Alchemical chart", level=43, xp=30,
             materials=[m(BOLT_OF_CLOTH, 2)], objectIds=[13662]),
        dict(id="astronomical_chart", name="Astronomical chart", level=63, xp=45,
             materials=[m(BOLT_OF_CLOTH, 3)], objectIds=[13663]),
        dict(id="infernal_chart", name="Infernal chart", level=83, xp=60,
             materials=[m(BOLT_OF_CLOTH, 4)], objectIds=[13664]),
    ],

    # --- Chapel ------------------------------------------------------------
    # Altars and statues come in one model per chapel alignment, so each tier lists the object ids
    # of all of its variants.
    "chapel_altar": [
        dict(id="oak_altar", name="Oak altar", level=45, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[13179, 13180, 13181, 40872],
             note="Prayer XP bonus 100%, up to 200% with both burners lit"),
        dict(id="teak_altar", name="Teak altar", level=50, xp=360,
             materials=[m(TEAK_PLANK, 4)], objectIds=[13182, 13183, 13184, 40873],
             note="Prayer XP bonus 110%, up to 210% with both burners lit"),
        dict(id="cloth_altar", name="Cloth altar", level=56, xp=390,
             materials=[m(TEAK_PLANK, 4), m(BOLT_OF_CLOTH, 2)],
             objectIds=[13185, 13186, 13187, 40874],
             note="Prayer XP bonus 125%, up to 225% with both burners lit"),
        dict(id="mahogany_altar", name="Mahogany altar", level=60, xp=590,
             materials=[m(MAHOGANY_PLANK, 4), m(BOLT_OF_CLOTH, 2)],
             objectIds=[13188, 13189, 13190, 40875],
             note="Prayer XP bonus 150%, up to 250% with both burners lit"),
        dict(id="limestone_altar", name="Limestone altar", level=64, xp=910,
             materials=[m(MAHOGANY_PLANK, 6), m(BOLT_OF_CLOTH, 2), m(LIMESTONE_BRICK, 2)],
             objectIds=[13191, 13192, 13193, 40876],
             note="Prayer XP bonus 175%, up to 275% with both burners lit"),
        dict(id="marble_altar", name="Marble altar", level=70, xp=1030,
             materials=[m(MARBLE_BLOCK, 2), m(BOLT_OF_CLOTH, 2)],
             objectIds=[13194, 13195, 13196, 40877],
             note="Prayer XP bonus 200%, up to 300% with both burners lit"),
        dict(id="gilded_altar", name="Gilded altar", level=75, xp=2230,
             materials=[m(MARBLE_BLOCK, 2), m(BOLT_OF_CLOTH, 2), m(GOLD_LEAF, 4)],
             objectIds=[13197, 13198, 13199, 40878],
             note="Prayer XP bonus 250%, up to 350% with both burners lit. The one most players want"),
    ],
    "chapel_lamp": [
        dict(id="steel_torches", name="Steel torches", level=45, xp=40,
             materials=[m(STEEL_BAR, 2)], objectIds=[13200, 13201], note="No Prayer bonus"),
        dict(id="wooden_torches", name="Wooden torches", level=49, xp=58,
             materials=[m(PLANK, 2), m(NAILS, 2)], objectIds=[13202, 13203], note="No Prayer bonus"),
        dict(id="steel_candlesticks", name="Steel candlesticks", level=53, xp=124,
             materials=[m(STEEL_BAR, 6), m(CANDLE, 6)], objectIds=[13204, 13205], note="No Prayer bonus"),
        dict(id="gold_candlesticks", name="Gold candlesticks", level=57, xp=46,
             materials=[m(GOLD_BAR, 6), m(CANDLE, 6)], objectIds=[13206, 13207], note="No Prayer bonus"),
        dict(id="oak_burners", name="Oak incense burners", level=61, xp=280,
             materials=[m(OAK_PLANK, 4), m(STEEL_BAR, 2)], objectIds=[13208, 13209],
             note="Light with a tinderbox and a clean marrentill for +50% Prayer XP each"),
        dict(id="mahogany_burners", name="Mahogany incense burners", level=65, xp=600,
             materials=[m(MAHOGANY_PLANK, 4), m(STEEL_BAR, 2)], objectIds=[13210, 13211],
             note="Light with a tinderbox and a clean marrentill for +50% Prayer XP each"),
        dict(id="marble_burners", name="Marble incense burners", level=69, xp=1600,
             materials=[m(MARBLE_BLOCK, 2), m(STEEL_BAR, 2)], objectIds=[13212, 13213],
             note="Light with a tinderbox and a clean marrentill for +50% Prayer XP each"),
    ],
    "chapel_icon": [
        dict(id="gnome_child_icon", name="Gnome child icon", level=45, xp=100,
             materials=[m(OAK_PLANK, 3)], objectIds=[40871], note="Also needs a Gnome child icon"),
        dict(id="guthix_symbol", name="Guthix symbol", level=48, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13174]),
        dict(id="saradomin_symbol", name="Saradomin symbol", level=48, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13172]),
        dict(id="zamorak_symbol", name="Zamorak symbol", level=48, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[13173]),
        dict(id="guthix_icon", name="Guthix icon", level=59, xp=960,
             materials=[m(TEAK_PLANK, 4), m(GOLD_LEAF, 2)], objectIds=[13177]),
        dict(id="saradomin_icon", name="Saradomin icon", level=59, xp=960,
             materials=[m(TEAK_PLANK, 4), m(GOLD_LEAF, 2)], objectIds=[13175]),
        dict(id="zamorak_icon", name="Zamorak icon", level=59, xp=960,
             materials=[m(TEAK_PLANK, 4), m(GOLD_LEAF, 2)], objectIds=[13176]),
        dict(id="bob_icon", name="Bob icon", level=71, xp=1160,
             materials=[m(MAHOGANY_PLANK, 4), m(GOLD_LEAF, 2)], objectIds=[13178],
             note="Also needs a Bob icon"),
    ],
    "chapel_musical": [
        dict(id="windchimes", name="Windchimes", level=49, xp=323,
             materials=[m(OAK_PLANK, 4), m(NAILS, 4), m(STEEL_BAR, 4)], objectIds=[13214]),
        dict(id="bells", name="Bells", level=58, xp=480,
             materials=[m(TEAK_PLANK, 4), m(STEEL_BAR, 6)], objectIds=[13215]),
        dict(id="organ", name="Organ", level=69, xp=680,
             materials=[m(MAHOGANY_PLANK, 4), m(STEEL_BAR, 6)], objectIds=[13216]),
    ],
    "chapel_statue": [
        dict(id="small_statue", name="Small statue", level=49, xp=40,
             materials=[m(LIMESTONE_BRICK, 2)], objectIds=[13271, 13274, 13277, 13280, 40915],
             note="Building one statue builds the other as well. " + ALIGN),
        dict(id="medium_statue", name="Medium statue", level=69, xp=500,
             materials=[m(MARBLE_BLOCK, 1)], objectIds=[13272, 13275, 13278, 13281, 40916],
             note="Building one statue builds the other as well. " + ALIGN),
        dict(id="large_statue", name="Large statue", level=89, xp=1500,
             materials=[m(MARBLE_BLOCK, 3)], objectIds=[13273, 13276, 13279, 13282, 40917],
             note="Building one statue builds the other as well. " + ALIGN),
    ],
    "chapel_window": [
        dict(id="shuttered_window", name="Shuttered window", level=49, xp=228,
             materials=[m(PLANK, 8), m(NAILS, 8)]),
        dict(id="decorative_window", name="Decorative window", level=69, xp=4,
             materials=[m(MOLTEN_GLASS, 8)]),
        dict(id="stained_glass", name="Stained glass", level=89, xp=5,
             materials=[m(MOLTEN_GLASS, 16)]),
    ],

    # --- Portal chamber ----------------------------------------------------
    # The frame is what costs materials. Where each portal points is chosen afterwards by casting
    # the teleport spell into it, so destinations are not part of a plan.
    "portal_frame": [
        dict(id="teak_portal", name="Teak portal", level=50, xp=270,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13636],
             note="Point it at a destination afterwards by casting that teleport at it"),
        dict(id="mahogany_portal", name="Mahogany portal", level=65, xp=420,
             materials=[m(MAHOGANY_PLANK, 3)], objectIds=[13637]),
        dict(id="marble_portal", name="Marble portal", level=80, xp=1500,
             materials=[m(MARBLE_BLOCK, 3)], objectIds=[13638]),
    ],
    "portal_centrepiece": [
        dict(id="teleport_focus", name="Teleport focus", level=50, xp=40,
             materials=[m(LIMESTONE_BRICK, 2)], note="Needed to aim the portals in this room"),
        dict(id="greater_teleport_focus", name="Greater teleport focus", level=65, xp=500,
             materials=[m(MARBLE_BLOCK, 1)]),
        dict(id="scrying_pool", name="Scrying pool", level=80, xp=2000,
             materials=[m(MARBLE_BLOCK, 4)]),
    ],
    # --- Portal nexus ------------------------------------------------------
    "nexus": [
        dict(id="marble_nexus", name="Marble portal nexus", level=72, xp=2000,
             materials=[m(MARBLE_BLOCK, 4)], objectIds=[33408],
             note="Destinations are added afterwards with runes; they are not part of the build"),
        dict(id="gilded_nexus", name="Gilded portal nexus", level=82, xp=2600,
             materials=[m(MARBLE_BLOCK, 8), m(GOLD_LEAF, 2)], objectIds=[33409],
             note="Upgrades the marble nexus; materials include that tier"),
        dict(id="crystalline_nexus", name="Crystalline portal nexus", level=92, xp=2600,
             materials=[m(MARBLE_BLOCK, 8), m(GOLD_LEAF, 4), m(MAGIC_STONE, 2)], objectIds=[33410],
             note="Upgrades the gilded nexus; materials include every tier below"),
    ],
    "nexus_amulet": [
        dict(id="mounted_xerics", name="Mounted Xeric's talisman", level=72, xp=500,
             materials=[m(MAHOGANY_PLANK, 1), m(GOLD_LEAF, 1)],
             note="Also needs an inert Xeric's talisman and 5,000 lizardman fangs"),
        dict(id="mounted_digsite", name="Mounted digsite pendant", level=82, xp=800,
             materials=[m(MAHOGANY_PLANK, 1), m(GOLD_LEAF, 1)],
             note="Also needs a curator's medallion"),
    ],
    # --- Quest hall --------------------------------------------------------
    "quest_portrait": [
        dict(id="king_arthur", name="King Arthur", level=35, xp=211,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13510], note="Also needs an Arthur portrait"),
        dict(id="elena", name="Elena", level=35, xp=211,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13511], note="Also needs an Elena portrait"),
        dict(id="giant_dwarf", name="Giant dwarf", level=35, xp=211,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13512], note="Also needs a Keldagrim portrait"),
        dict(id="miscellanians", name="Miscellanians", level=55, xp=311,
             materials=[m(MAHOGANY_PLANK, 2)], objectIds=[13513], note="Also needs a Misc. portrait"),
    ],
    "quest_landscape": [
        dict(id="lumbridge_painting", name="Lumbridge", level=44, xp=314,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13517], note="Also needs a Lumbridge painting"),
        dict(id="desert_painting", name="The Desert", level=44, xp=314,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13514], note="Also needs a Desert painting"),
        dict(id="morytania_painting", name="Morytania", level=44, xp=314,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13518], note="Also needs a Morytania painting"),
        dict(id="karamja_painting", name="Karamja", level=65, xp=464,
             materials=[m(MAHOGANY_PLANK, 3)], objectIds=[13516], note="Also needs a Karamja painting"),
        dict(id="isafdar_painting", name="Isafdar", level=65, xp=464,
             materials=[m(MAHOGANY_PLANK, 3)], objectIds=[13515], note="Also needs an Isafdar painting"),
    ],
    "quest_guild_trophy": [
        dict(id="anti_dragon_shield_trophy", name="Anti-dragon shield", level=47, xp=280,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13522], note="Also needs an anti-dragon shield"),
        dict(id="amulet_of_glory_trophy", name="Amulet of glory", level=47, xp=290,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13523],
             note="Also needs an uncharged amulet of glory"),
        dict(id="cape_of_legends_trophy", name="Cape of Legends", level=47, xp=300,
             materials=[m(TEAK_PLANK, 3)], objectIds=[13524], note="Also needs a Cape of Legends"),
        dict(id="mythical_cape_trophy", name="Mythical cape", level=47, xp=370,
             materials=[m(TEAK_PLANK, 3)], objectIds=[31986],
             note="Also needs a mythical cape, and Dragon Slayer II. A popular training method"),
    ],
    "quest_sword": [
        dict(id="silverlight_trophy", name="Silverlight", level=42, xp=187,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13519], note="Also needs Silverlight"),
        dict(id="excalibur_trophy", name="Excalibur", level=42, xp=194,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13521], note="Also needs Excalibur"),
        dict(id="darklight_trophy", name="Darklight", level=42, xp=202,
             materials=[m(TEAK_PLANK, 2)], objectIds=[13520], note="Also needs Darklight"),
    ],
    "quest_map": [
        dict(id="small_map", name="Small map", level=38, xp=211,
             materials=[m(TEAK_PLANK, 2)], note="Also needs a small map"),
        dict(id="medium_map", name="Medium map", level=58, xp=451,
             materials=[m(MAHOGANY_PLANK, 3)], note="Also needs a medium map"),
        dict(id="large_map", name="Large map", level=78, xp=591,
             materials=[m(MAHOGANY_PLANK, 4)], note="Also needs a large map"),
    ],
    # --- Costume room ------------------------------------------------------
    # Every costume storage space upgrades in place, so materials are cumulative.
    "costume_cape_rack": [
        dict(id="oak_cape_rack", name="Oak cape rack", level=54, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[18766]),
        dict(id="teak_cape_rack", name="Teak cape rack", level=63, xp=360,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4)], objectIds=[18767]),
        dict(id="mahogany_cape_rack", name="Mahogany cape rack", level=72, xp=560,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 4)], objectIds=[18768]),
        dict(id="gilded_cape_rack", name="Gilded cape rack", level=81, xp=860,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 8), m(GOLD_LEAF, 1)],
             objectIds=[18769]),
        dict(id="marble_cape_rack", name="Marble cape rack", level=90, xp=500,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 8), m(GOLD_LEAF, 1),
                        m(MARBLE_BLOCK, 1)], objectIds=[18770]),
        dict(id="magic_cape_rack", name="Magical cape rack", level=99, xp=1000,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 8), m(GOLD_LEAF, 1),
                        m(MARBLE_BLOCK, 1), m(MAGIC_STONE, 1)], objectIds=[18771]),
    ],
    "costume_wardrobe": [
        dict(id="oak_wardrobe_c", name="Oak magic wardrobe", level=42, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[18784, 18785]),
        dict(id="carved_oak_wardrobe", name="Carved oak magic wardrobe", level=51, xp=360,
             materials=[m(OAK_PLANK, 10)], objectIds=[18786, 18787]),
        dict(id="teak_wardrobe_c", name="Teak magic wardrobe", level=60, xp=360,
             materials=[m(OAK_PLANK, 10), m(TEAK_PLANK, 4)], objectIds=[18788, 18789]),
        dict(id="carved_teak_wardrobe", name="Carved teak magic wardrobe", level=69, xp=540,
             materials=[m(OAK_PLANK, 10), m(TEAK_PLANK, 10)], objectIds=[18790, 18791]),
        dict(id="mahogany_wardrobe_c", name="Mahogany magic wardrobe", level=78, xp=560,
             materials=[m(OAK_PLANK, 10), m(TEAK_PLANK, 10), m(MAHOGANY_PLANK, 4)],
             objectIds=[18792, 18793]),
        dict(id="gilded_wardrobe_c", name="Gilded magic wardrobe", level=87, xp=860,
             materials=[m(OAK_PLANK, 10), m(TEAK_PLANK, 10), m(MAHOGANY_PLANK, 8), m(GOLD_LEAF, 1)],
             objectIds=[18794, 18795]),
        dict(id="marble_wardrobe_c", name="Marble magic wardrobe", level=96, xp=500,
             materials=[m(OAK_PLANK, 10), m(TEAK_PLANK, 10), m(MAHOGANY_PLANK, 8), m(GOLD_LEAF, 1),
                        m(MARBLE_BLOCK, 1)], objectIds=[18796, 18797]),
    ],
    "costume_toy_box": [
        dict(id="oak_toy_box", name="Oak toy box", level=50, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[18798, 18799]),
        dict(id="teak_toy_box", name="Teak toy box", level=68, xp=180,
             materials=[m(TEAK_PLANK, 2)], objectIds=[18800, 18801]),
        dict(id="mahogany_toy_box", name="Mahogany toy box", level=86, xp=280,
             materials=[m(MAHOGANY_PLANK, 2)], objectIds=[18802, 18803]),
    ],
    "costume_treasure_chest": [
        dict(id="oak_treasure_chest", name="Oak treasure chest", level=48, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[18804, 18805]),
        dict(id="teak_treasure_chest", name="Teak treasure chest", level=66, xp=180,
             materials=[m(OAK_PLANK, 2), m(TEAK_PLANK, 2)], objectIds=[18806, 18807]),
        dict(id="mahogany_treasure_chest", name="Mahogany treasure chest", level=84, xp=280,
             materials=[m(OAK_PLANK, 2), m(TEAK_PLANK, 2), m(MAHOGANY_PLANK, 2)],
             objectIds=[18808, 18809]),
    ],
    "costume_fancy_dress": [
        dict(id="oak_fancy_dress", name="Oak fancy dress box", level=44, xp=120,
             materials=[m(OAK_PLANK, 2)], objectIds=[18772, 18773]),
        dict(id="teak_fancy_dress", name="Teak fancy dress box", level=62, xp=180,
             materials=[m(OAK_PLANK, 2), m(TEAK_PLANK, 2)], objectIds=[18774, 18775]),
        dict(id="mahogany_fancy_dress", name="Mahogany fancy dress box", level=80, xp=280,
             materials=[m(OAK_PLANK, 2), m(TEAK_PLANK, 2), m(MAHOGANY_PLANK, 2)],
             objectIds=[18776, 18777]),
    ],
    "costume_armour_case": [
        dict(id="oak_armour_case", name="Oak armour case", level=46, xp=180,
             materials=[m(OAK_PLANK, 3)], objectIds=[18778, 18779]),
        dict(id="teak_armour_case", name="Teak armour case", level=64, xp=270,
             materials=[m(OAK_PLANK, 3), m(TEAK_PLANK, 3)], objectIds=[18780, 18781]),
        dict(id="mahogany_armour_case", name="Mahogany armour case", level=82, xp=420,
             materials=[m(OAK_PLANK, 3), m(TEAK_PLANK, 3), m(MAHOGANY_PLANK, 3)],
             objectIds=[18782, 18783]),
    ],

    # --- Achievement gallery -----------------------------------------------
    "achv_altar": [
        dict(id="ancient_altar", name="Ancient altar", level=80, xp=1490,
             materials=[m(LIMESTONE_BRICK, 10), m(MAGIC_STONE, 1)], objectIds=[29147],
             note="Also needs an ancient signet and a pharaoh's sceptre"),
        dict(id="lunar_altar", name="Lunar altar", level=80, xp=1957,
             materials=[m(LIMESTONE_BRICK, 10), m(MAGIC_STONE, 1)], objectIds=[29148],
             note="Also needs a lunar signet and 10,000 astral runes"),
        dict(id="dark_altar", name="Dark altar", level=80, xp=3888,
             materials=[m(LIMESTONE_BRICK, 10), m(MAGIC_STONE, 1)], objectIds=[29149],
             note="Also needs an arceuus signet, 5,000 blood runes and 5,000 soul runes"),
        dict(id="occult_altar", name="Occult altar", level=90, xp=3445,
             materials=[m(LIMESTONE_BRICK, 10), m(MAGIC_STONE, 1)],
             objectIds=[31858, 31859, 31860, 31861],
             note="Combines the other three altars, so it needs all of their signets and runes too"),
    ],
    "achv_log": [
        dict(id="mahogany_adventure_log", name="Mahogany adventure log", level=83, xp=504,
             materials=[m(MAHOGANY_PLANK, 3), m(PAPYRUS, 2)], objectIds=[29151],
             note="Also needs an enchanted gem"),
        dict(id="gilded_adventure_log", name="Gilded adventure log", level=88, xp=1100,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 2)], objectIds=[29152],
             note="Also needs an enchanted gem"),
        dict(id="marble_adventure_log", name="Marble adventure log", level=93, xp=1160,
             materials=[m(MARBLE_BLOCK, 2), m(LIMESTONE_BRICK, 4)], objectIds=[29153],
             note="Also needs an enchanted gem"),
    ],
    "achv_jewellery": [
        dict(id="basic_jewellery_box", name="Basic jewellery box", level=81, xp=605,
             materials=[m(BOLT_OF_CLOTH, 1), m(STEEL_BAR, 1)],
             note="Also needs 3 games necklaces (8) and 3 rings of dueling (8)"),
        dict(id="fancy_jewellery_box", name="Fancy jewellery box", level=86, xp=1350,
             materials=[m(BOLT_OF_CLOTH, 1), m(STEEL_BAR, 1), m(GOLD_LEAF, 1)],
             note="Upgrades the basic box; also needs 5 skills necklaces (4) and 5 combat bracelets (4)"),
        dict(id="ornate_jewellery_box", name="Ornate jewellery box", level=91, xp=2680,
             materials=[m(BOLT_OF_CLOTH, 1), m(STEEL_BAR, 1), m(GOLD_LEAF, 3)],
             note="Upgrades the fancy box; also needs 8 amulets of glory (4) and 8 rings of wealth (5)"),
    ],
    "achv_lair": [
        dict(id="boss_lair_display", name="Boss lair display", level=87, xp=1483,
             materials=[m(STEEL_BAR, 4), m(MOLTEN_GLASS, 5), m(MAHOGANY_PLANK, 10)],
             objectIds=[29157],
             note="Which boss it shows is chosen afterwards from the ones you have killed"),
    ],
    "achv_display": [
        dict(id="mounted_emblem", name="Mounted emblem", level=80, xp=5300,
             materials=[m(MARBLE_BLOCK, 1), m(GOLD_LEAF, 1)],
             note="Also needs a decorative emblem"),
        dict(id="mounted_coins", name="Mounted coins", level=80, xp=800,
             materials=[m(MARBLE_BLOCK, 1), m(GOLD_LEAF, 1)], coins=100000000,
             note="Yes, one hundred million coins"),
        dict(id="cape_hanger", name="Cape hanger", level=80, xp=800,
             materials=[m(MARBLE_BLOCK, 1), m(GOLD_LEAF, 1)]),
    ],
    "achv_questlist": [
        dict(id="quest_list", name="Quest list", level=80, xp=310,
             materials=[m(PAPYRUS, 10), m(GOLD_LEAF, 1)]),
    ],
    # --- Superior garden ---------------------------------------------------
    "sg_teleport": [
        dict(id="spirit_tree_sg", name="Spirit tree", level=75, xp=350,
             materials=[], note="Needs a spirit sapling. Also gives 350 Farming experience"),
        dict(id="obelisk_sg", name="Obelisk", level=80, xp=3000,
             materials=[m(MARBLE_BLOCK, 4)], note="Also needs 4 ancient crystals"),
        dict(id="fairy_ring_sg", name="Fairy ring", level=85, xp=535,
             materials=[m(MUSHROOM, 10)], note="Also needs a fairy enchantment"),
        dict(id="spirit_tree_fairy_ring", name="Spirit tree and fairy ring", level=95, xp=885,
             materials=[m(MUSHROOM, 10)],
             note="Needs a spirit sapling and a fairy enchantment. Gives Construction and Farming XP"),
    ],
    "sg_topiary": [
        dict(id="topiary_bush", name="Topiary bush", level=65, xp=141,
             materials=[], objectIds=[29230],
             note="Needs a bagged topiary hedge. Also gives 141 Farming experience"),
    ],
    "sg_pool": [
        dict(id="restoration_pool", name="Restoration pool", level=65, xp=706,
             materials=[m(LIMESTONE_BRICK, 5), m(BUCKET_OF_WATER, 5)], objectIds=[29237],
             note="Also needs 1,000 soul runes and 1,000 body runes"),
        dict(id="revitalisation_pool", name="Revitalisation pool", level=70, xp=850,
             materials=[m(LIMESTONE_BRICK, 5), m(BUCKET_OF_WATER, 5)], objectIds=[29238],
             note="Upgrades the restoration pool; also needs its runes plus 10 stamina potions (4)"),
        dict(id="rejuvenation_pool", name="Rejuvenation pool", level=80, xp=900,
             materials=[m(LIMESTONE_BRICK, 5), m(BUCKET_OF_WATER, 5)], objectIds=[29239],
             note="Upgrades the revitalisation pool; also needs 10 prayer potions (4)"),
        dict(id="fancy_rejuvenation_pool", name="Fancy rejuvenation pool", level=85, xp=1950,
             materials=[m(LIMESTONE_BRICK, 5), m(BUCKET_OF_WATER, 5), m(MARBLE_BLOCK, 2)],
             objectIds=[29240], note="Also needs 10 super restores (4)"),
        dict(id="ornate_rejuvenation_pool", name="Ornate rejuvenation pool", level=90, xp=3107,
             materials=[m(LIMESTONE_BRICK, 5), m(BUCKET_OF_WATER, 5), m(MARBLE_BLOCK, 2),
                        m(GOLD_LEAF, 5)], objectIds=[29241],
             note="The one most players want: full restore plus cure. Also needs 10 anti-venom (4) "
                  "and 1,000 blood runes"),
    ],
    "sg_theme": [
        dict(id="zen_theme", name="Zen theme", level=65, xp=474,
             materials=[m(BUCKET_OF_SAND, 6), m(PINK_DYE, 1)], note="Also needs a bagged nice tree"),
        dict(id="otherworldly_theme", name="Otherworldly theme", level=75, xp=316,
             materials=[m(SUPERCOMPOST, 8), m(BLUE_DYE, 1), m(MUSHROOM, 4)],
             note="Also needs magic secateurs"),
        dict(id="volcanic_theme", name="Volcanic theme", level=85, xp=4464,
             materials=[m(GRANITE_5KG, 2), m(ONYX, 6)],
             note="Also needs 1,000 fire runes and 2,000 lava runes"),
    ],
    "sg_fence": [
        dict(id="redwood_fence", name="Redwood fence", level=75, xp=240,
             materials=[m(REDWOOD_LOGS, 10), m(STEEL_BAR, 2)]),
        dict(id="marble_wall_sg", name="Marble wall", level=79, xp=4000,
             materials=[m(MARBLE_BLOCK, 8)]),
        dict(id="obsidian_fence", name="Obsidian fence", level=83, xp=2741,
             materials=[],
             note="Needs 10 toktz-mej-tal, 2 tzhaar-ket-om and 25 toktz-xil-ul"),
    ],
    "sg_seating": [
        dict(id="teak_garden_bench", name="Teak garden bench", level=66, xp=540,
             materials=[m(TEAK_PLANK, 6)], note="A well-known Construction training method"),
        dict(id="gnome_bench", name="Gnome bench", level=77, xp=840,
             materials=[m(MAHOGANY_PLANK, 6)]),
        dict(id="marble_bench", name="Marble decorative bench", level=88, xp=3000,
             materials=[m(MARBLE_BLOCK, 6)]),
        dict(id="obsidian_bench", name="Obsidian decorative bench", level=98, xp=2331,
             materials=[m(MARBLE_BLOCK, 3), m(ONYX, 1)],
             note="Also needs 250 fire runes and 500 lava runes"),
    ],

    # --- Combat room -------------------------------------------------------
    "combat_ring": [
        dict(id="boxing_ring", name="Boxing ring", level=32, xp=420,
             materials=[m(OAK_PLANK, 6), m(BOLT_OF_CLOTH, 4)]),
        dict(id="fencing_ring", name="Fencing ring", level=41, xp=570,
             materials=[m(OAK_PLANK, 8), m(BOLT_OF_CLOTH, 6)]),
        dict(id="combat_ring_c", name="Combat ring", level=51, xp=630,
             materials=[m(TEAK_PLANK, 6), m(BOLT_OF_CLOTH, 6)]),
        dict(id="ranging_pedestals", name="Ranging pedestals", level=71, xp=720,
             materials=[m(TEAK_PLANK, 8)]),
        dict(id="balance_beam", name="Balance beam", level=81, xp=1000,
             materials=[m(TEAK_PLANK, 10), m(STEEL_BAR, 5)]),
    ],
    "combat_storage": [
        dict(id="boxing_glove_rack", name="Boxing glove rack", level=34, xp=120,
             materials=[m(OAK_PLANK, 2)]),
        dict(id="weapons_rack", name="Weapons rack", level=44, xp=180,
             materials=[m(TEAK_PLANK, 2)]),
        dict(id="extra_weapons_rack", name="Extra weapons rack", level=54, xp=440,
             materials=[m(TEAK_PLANK, 4), m(STEEL_BAR, 4)]),
    ],
    "combat_dummy": [
        dict(id="combat_dummy", name="Combat dummy", level=48, xp=660,
             materials=[m(TEAK_PLANK, 5), m(BOLT_OF_CLOTH, 4), m(BUCKET_OF_SAND, 5)]),
        dict(id="undead_combat_dummy", name="Undead combat dummy", level=53, xp=220,
             materials=[m(TEAK_PLANK, 5), m(BOLT_OF_CLOTH, 4), m(BUCKET_OF_SAND, 5)],
             note="Upgrades the combat dummy; also needs a black mask and 4 buckets of slime"),
        dict(id="ornate_undead_dummy", name="Ornate undead combat dummy", level=58, xp=300,
             materials=[m(TEAK_PLANK, 5), m(BOLT_OF_CLOTH, 4), m(BUCKET_OF_SAND, 5), m(GOLD_LEAF, 1)],
             objectIds=[9355], note="Upgrades the undead dummy; materials include every tier below"),
    ],
    # --- Games room --------------------------------------------------------
    "games_game": [
        dict(id="jester", name="Jester", level=39, xp=360, materials=[m(TEAK_PLANK, 4)]),
        dict(id="treasure_hunt", name="Treasure hunt", level=49, xp=800,
             materials=[m(TEAK_PLANK, 8), m(STEEL_BAR, 4)]),
        dict(id="hangman", name="Hangman", level=59, xp=1200,
             materials=[m(TEAK_PLANK, 12), m(STEEL_BAR, 6)]),
    ],
    "games_prize": [
        dict(id="oak_prize_chest", name="Oak prize chest", level=34, xp=240,
             materials=[m(OAK_PLANK, 4)]),
        dict(id="teak_prize_chest", name="Teak prize chest", level=44, xp=660,
             materials=[m(TEAK_PLANK, 4), m(GOLD_LEAF, 1)]),
        dict(id="mahogany_prize_chest", name="Mahogany prize chest", level=54, xp=860,
             materials=[m(MAHOGANY_PLANK, 4), m(GOLD_LEAF, 1)]),
    ],
    "games_stone": [
        dict(id="clay_attack_stone", name="Clay attack stone", level=39, xp=100,
             materials=[m(SOFT_CLAY, 10)]),
        dict(id="limestone_attack_stone", name="Limestone attack stone", level=59, xp=200,
             materials=[m(LIMESTONE_BRICK, 10)]),
        dict(id="marble_attack_stone", name="Marble attack stone", level=79, xp=2000,
             materials=[m(MARBLE_BLOCK, 4)]),
    ],
    "games_elemental": [
        dict(id="lesser_balance", name="Lesser magical balance", level=37, xp=176,
             materials=[], note="Needs 500 each of air, earth, fire and water runes"),
        dict(id="medium_balance", name="Medium magical balance", level=57, xp=252,
             materials=[], note="Needs 1,000 each of air, earth, fire and water runes"),
        dict(id="greater_balance", name="Greater magical balance", level=77, xp=356,
             materials=[], note="Needs 2,000 each of air, earth, fire and water runes"),
    ],
    "games_ranging": [
        dict(id="hoop_and_stick", name="Hoop and stick", level=30, xp=120,
             materials=[m(OAK_PLANK, 2)]),
        dict(id="dartboard", name="Dartboard", level=54, xp=290,
             materials=[m(TEAK_PLANK, 3), m(STEEL_BAR, 1)]),
        dict(id="archery_target", name="Archery target", level=81, xp=600,
             materials=[m(TEAK_PLANK, 6), m(STEEL_BAR, 3)]),
    ],
    # --- Formal garden (the two plant sets are each shared by one big and one small space) -----------------------------------------------------
    "fg_centrepiece": [
        dict(id="exit_portal_fg", name="Exit portal", level=1, xp=100,
             materials=[m(IRON_BAR, 10)],
             note="Every house needs one exit portal, in a garden or formal garden"),
        dict(id="gazebo", name="Gazebo", level=65, xp=1200,
             materials=[m(MAHOGANY_PLANK, 8), m(STEEL_BAR, 4)]),
        dict(id="dungeon_entrance_fg", name="Dungeon entrance", level=70, xp=500,
             materials=[m(MARBLE_BLOCK, 1)], note="Needed to reach the dungeon floor"),
        dict(id="small_fountain", name="Small fountain", level=71, xp=500,
             materials=[m(MARBLE_BLOCK, 1)]),
        dict(id="large_fountain", name="Large fountain", level=75, xp=1000,
             materials=[m(MARBLE_BLOCK, 2)]),
        dict(id="posh_fountain", name="Posh fountain", level=81, xp=1500,
             materials=[m(MARBLE_BLOCK, 3)]),
    ],
    "fg_fencing": [
        dict(id="boundary_stones", name="Boundary stones", level=55, xp=100,
             materials=[m(SOFT_CLAY, 10)], objectIds=[5152]),
        dict(id="wooden_fence", name="Wooden fence", level=59, xp=280,
             materials=[m(PLANK, 10)], objectIds=[5153]),
        dict(id="stone_wall", name="Stone wall", level=63, xp=200,
             materials=[m(LIMESTONE_BRICK, 10)], objectIds=[5154]),
        dict(id="iron_railings", name="Iron railings", level=67, xp=220,
             materials=[m(IRON_BAR, 10), m(LIMESTONE_BRICK, 6)], objectIds=[5155]),
        dict(id="picket_fence", name="Picket fence", level=71, xp=640,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 2)], objectIds=[5631]),
        dict(id="garden_fence", name="Garden fence", level=75, xp=940,
             materials=[m(TEAK_PLANK, 10), m(STEEL_BAR, 2)], objectIds=[5632]),
        dict(id="marble_wall_fg", name="Marble wall", level=79, xp=4000,
             materials=[m(MARBLE_BLOCK, 8)], objectIds=[5907]),
    ],
    "fg_hedging": [
        dict(id="thorny_hedge", name="Thorny hedge", level=56, xp=70, materials=[],
             note="Needs a bagged thorny hedge, and a filled watering can"),
        dict(id="nice_hedge", name="Nice hedge", level=60, xp=100, materials=[],
             note="Needs a bagged nice hedge"),
        dict(id="small_box_hedge", name="Small box hedge", level=64, xp=122, materials=[],
             note="Needs a bagged small box hedge"),
        dict(id="topiary_hedge", name="Topiary hedge", level=68, xp=141, materials=[],
             note="Needs a bagged topiary hedge"),
        dict(id="fancy_hedge", name="Fancy hedge", level=72, xp=158, materials=[],
             note="Needs a bagged fancy hedge"),
        dict(id="tall_fancy_hedge", name="Tall fancy hedge", level=76, xp=223, materials=[],
             note="Needs a bagged tall fancy hedge"),
        dict(id="tall_box_hedge", name="Tall box hedge", level=80, xp=316, materials=[],
             note="Needs a bagged tall box hedge"),
    ],
    "fg_plant_set_1": [
        dict(id="sunflower", name="Sunflower", level=66, xp=70, materials=[],
             note="Needs a bagged sunflower, and a filled watering can"),
        dict(id="marigolds", name="Marigolds", level=71, xp=100, materials=[],
             note="Needs bagged marigolds"),
        dict(id="roses", name="Roses", level=76, xp=122, materials=[], note="Needs bagged roses"),
    ],
    "fg_plant_set_2": [
        dict(id="rosemary", name="Rosemary", level=66, xp=70, materials=[],
             note="Needs a bagged flower, and a filled watering can"),
        dict(id="daffodils", name="Daffodils", level=71, xp=100, materials=[],
             note="Needs bagged daffodils"),
        dict(id="bluebells", name="Bluebells", level=76, xp=122, materials=[],
             note="Needs bagged bluebells"),
    ],

    # --- Throne room -------------------------------------------------------
    "throne_throne": [
        dict(id="oak_throne", name="Oak throne", level=60, xp=800,
             materials=[m(OAK_PLANK, 5), m(MARBLE_BLOCK, 1)]),
        dict(id="teak_throne", name="Teak throne", level=67, xp=1450,
             materials=[m(TEAK_PLANK, 5), m(MARBLE_BLOCK, 2)]),
        dict(id="mahogany_throne", name="Mahogany throne", level=74, xp=2200,
             materials=[m(MAHOGANY_PLANK, 5), m(MARBLE_BLOCK, 3)]),
        dict(id="gilded_throne", name="Gilded throne", level=81, xp=2600,
             materials=[m(MAHOGANY_PLANK, 5), m(MARBLE_BLOCK, 2), m(GOLD_LEAF, 3)]),
        dict(id="skeleton_throne", name="Skeleton throne", level=88, xp=7003,
             materials=[m(MAGIC_STONE, 5), m(MARBLE_BLOCK, 4), m(BONES, 5), m(SKULL, 2)]),
        dict(id="crystal_throne", name="Crystal throne", level=95, xp=15000,
             materials=[m(MAGIC_STONE, 15)]),
        dict(id="demonic_throne", name="Demonic throne", level=99, xp=25000,
             materials=[m(MAGIC_STONE, 25)], note="The most expensive single item in the house"),
    ],
    "throne_floor": [
        dict(id="floor_decoration", name="Floor decoration", level=61, xp=700,
             materials=[m(MAHOGANY_PLANK, 5)]),
        dict(id="steel_cage_floor", name="Steel cage", level=68, xp=1100,
             materials=[m(MAHOGANY_PLANK, 5), m(STEEL_BAR, 20)]),
        dict(id="trapdoor_floor", name="Trapdoor", level=74, xp=770,
             materials=[m(MAHOGANY_PLANK, 5), m(CLOCKWORK, 10)]),
        dict(id="lesser_magic_cage", name="Lesser magic cage", level=82, xp=2700,
             materials=[m(MAHOGANY_PLANK, 5), m(MAGIC_STONE, 2)]),
        dict(id="greater_magic_cage", name="Greater magic cage", level=89, xp=4700,
             materials=[m(MAHOGANY_PLANK, 5), m(MAGIC_STONE, 4)]),
    ],
    "throne_lever": [
        dict(id="oak_lever", name="Oak lever", level=68, xp=300, materials=[m(OAK_PLANK, 5)]),
        dict(id="teak_lever", name="Teak lever", level=78, xp=450, materials=[m(TEAK_PLANK, 5)]),
        dict(id="mahogany_lever", name="Mahogany lever", level=88, xp=700,
             materials=[m(MAHOGANY_PLANK, 5)]),
    ],
    "throne_trapdoor": [
        dict(id="oak_trapdoor", name="Oak trapdoor", level=68, xp=300, materials=[m(OAK_PLANK, 5)]),
        dict(id="teak_trapdoor", name="Teak trapdoor", level=78, xp=450, materials=[m(TEAK_PLANK, 5)]),
        dict(id="mahogany_trapdoor", name="Mahogany trapdoor", level=88, xp=700,
             materials=[m(MAHOGANY_PLANK, 5)]),
    ],
    "throne_decoration": [
        dict(id="oak_wall_decoration_t", name="Oak wall decoration", level=16, xp=120,
             materials=[m(OAK_PLANK, 2)], note="Needs a family crest from Sir Renitee"),
        dict(id="teak_wall_decoration_t", name="Teak wall decoration", level=36, xp=180,
             materials=[m(TEAK_PLANK, 2)], note="Needs a family crest from Sir Renitee"),
        dict(id="gilded_decoration_t", name="Gilded decoration", level=56, xp=1020,
             materials=[m(MAHOGANY_PLANK, 3), m(GOLD_LEAF, 2)],
             note="Needs a family crest from Sir Renitee"),
        dict(id="round_shield", name="Round shield", level=66, xp=120, materials=[m(OAK_PLANK, 2)]),
        dict(id="square_shield", name="Square shield", level=76, xp=360, materials=[m(TEAK_PLANK, 4)]),
        dict(id="kite_shield", name="Kite shield", level=86, xp=420,
             materials=[m(MAHOGANY_PLANK, 3)]),
    ],
    # --- Menagerie ---------------------------------------------------------
    "men_pethouse": [
        dict(id="oak_pet_house", name="Oak house", level=37, xp=240,
             materials=[m(OAK_PLANK, 4)], objectIds=[26297]),
        dict(id="teak_pet_house", name="Teak house", level=48, xp=360,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4)], objectIds=[26298],
             note="Upgrades the oak house; materials include that tier"),
        dict(id="mahogany_pet_house", name="Mahogany house", level=59, xp=560,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 4)], objectIds=[26299],
             note="Materials include every tier below"),
        dict(id="consecrated_pet_house", name="Consecrated house", level=70, xp=1560,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 8), m(MAGIC_STONE, 1)],
             objectIds=[26830], note="Materials include every tier below"),
        dict(id="desecrated_pet_house", name="Desecrated house", level=81, xp=160,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 9), m(MAGIC_STONE, 1),
                        m(LIMESTONE_BRICK, 1)], objectIds=[26831],
             note="Materials include every tier below"),
        dict(id="nature_pet_house", name="Nature house", level=92, xp=158,
             materials=[m(OAK_PLANK, 4), m(TEAK_PLANK, 4), m(MAHOGANY_PLANK, 10), m(MAGIC_STONE, 1),
                        m(LIMESTONE_BRICK, 1), m(BUCKET_OF_WATER, 2), m(SUPERCOMPOST, 3)],
             objectIds=[26832], note="Materials include every tier below"),
    ],
    "men_habitat": [
        dict(id="grassland_habitat", name="Grassland habitat", level=37, xp=37,
             materials=[m(COMPOST, 2)], objectIds=[26834, 26840, 26846, 26852],
             note="Also needs a bagged dead tree"),
        dict(id="forest_habitat", name="Forest habitat", level=47, xp=51,
             materials=[m(COMPOST, 3)], objectIds=[26835, 26841, 26847, 26853],
             note="Also needs a bagged nice tree"),
        dict(id="desert_habitat", name="Desert habitat", level=57, xp=181,
             materials=[m(BUCKET_OF_SAND, 5)], objectIds=[26836, 26842, 26848, 26854],
             note="Also needs a bagged plant 1"),
        dict(id="polar_habitat", name="Polar habitat", level=67, xp=271,
             materials=[m(OAK_PLANK, 3)], objectIds=[26837, 26843, 26849, 26855],
             note="Also needs 2,000 water runes and 5 ice coolers"),
        dict(id="volcanic_habitat", name="Volcanic habitat", level=77, xp=46,
             materials=[m(GRANITE_5KG, 5)], objectIds=[26838, 26844, 26850, 26856],
             note="Also needs 100 lava runes"),
    ],
    "men_scratch": [
        dict(id="oak_scratching_post", name="Oak scratching post", level=39, xp=124,
             materials=[m(OAK_PLANK, 2), m(ROPE, 1)], objectIds=[26858]),
        dict(id="teak_scratching_post", name="Teak scratching post", level=49, xp=204,
             materials=[m(TEAK_PLANK, 2), m(ROPE, 1), m(LIMESTONE_BRICK, 1)], objectIds=[26859]),
        dict(id="mahogany_scratching_post", name="Mahogany scratching post", level=59, xp=304,
             materials=[m(MAHOGANY_PLANK, 2), m(ROPE, 1), m(LIMESTONE_BRICK, 1)], objectIds=[26860]),
    ],
    "men_arena": [
        dict(id="simple_arena", name="Simple arena", level=63, xp=139,
             materials=[m(OAK_PLANK, 2), m(BOLT_OF_CLOTH, 1), m(ROPE, 1)], objectIds=[26862]),
        dict(id="advanced_arena", name="Advanced arena", level=73, xp=199,
             materials=[m(TEAK_PLANK, 2), m(BOLT_OF_CLOTH, 1), m(ROPE, 1)], objectIds=[26863]),
        dict(id="glorious_arena", name="Glorious arena", level=83, xp=299,
             materials=[m(MAHOGANY_PLANK, 2), m(BOLT_OF_CLOTH, 1), m(ROPE, 1)], objectIds=[26864]),
    ],
    "men_petlist": [
        dict(id="pet_list", name="Pet list", level=38, xp=198,
             materials=[m(OAK_PLANK, 3), m(BOLT_OF_CLOTH, 1), m(PAPYRUS, 1)], objectIds=[26868]),
    ],
    "men_feeder": [
        dict(id="oak_feeder", name="Oak feeder", level=37, xp=182,
             materials=[m(OAK_PLANK, 3), m(BUCKET_OF_MILK, 1)], objectIds=[26870]),
        dict(id="teak_feeder", name="Teak feeder", level=48, xp=272,
             materials=[m(TEAK_PLANK, 3), m(BUCKET_OF_MILK, 1)], objectIds=[26871]),
        dict(id="mahogany_feeder", name="Mahogany feeder", level=59, xp=862,
             materials=[m(MAHOGANY_PLANK, 4), m(BUCKET_OF_MILK, 1), m(GOLD_LEAF, 1)],
             objectIds=[26872]),
    ],

    # --- Dungeon, oubliette and treasure room ------------------------------
    # Guards, traps and monsters are bought outright rather than built from materials, so they
    # carry a coin cost instead.
    "dun_guard": [
        dict(id="skeleton_guard", name="Skeleton guard", level=70, xp=223, materials=[], coins=50000),
        dict(id="guard_dog", name="Guard dog", level=74, xp=273, materials=[], coins=75000),
        dict(id="hobgoblin_guard", name="Hobgoblin", level=78, xp=316, materials=[], coins=100000),
        dict(id="baby_red_dragon_guard", name="Baby red dragon", level=82, xp=387, materials=[],
             coins=150000),
        dict(id="huge_spider_guard", name="Huge spider", level=86, xp=447, materials=[], coins=200000),
        dict(id="troll_guard", name="Troll guard", level=90, xp=1000, materials=[], coins=1000000),
        dict(id="hellhound_guard", name="Hellhound", level=94, xp=2236, materials=[], coins=5000000),
    ],
    "dun_trap": [
        dict(id="spike_trap", name="Spike trap", level=72, xp=223, materials=[], coins=50000),
        dict(id="man_trap", name="Man trap", level=76, xp=273, materials=[], coins=75000),
        dict(id="tangle_vine", name="Tangle vine", level=80, xp=316, materials=[], coins=100000),
        dict(id="marble_trap", name="Marble trap", level=84, xp=387, materials=[], coins=150000),
        dict(id="teleport_trap", name="Teleport trap", level=88, xp=447, materials=[], coins=200000),
    ],
    "dun_door": [
        dict(id="oak_door", name="Oak door", level=74, xp=600, materials=[m(OAK_PLANK, 10)],
             note="A well-known Construction training method"),
        dict(id="steel_plated_door", name="Steel-plated door", level=84, xp=800,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 10)]),
        dict(id="marble_door", name="Marble door", level=94, xp=2000, materials=[m(MARBLE_BLOCK, 4)]),
    ],
    "dun_lighting": [
        dict(id="dun_candle", name="Candle", level=72, xp=243,
             materials=[m(OAK_PLANK, 4), m(LIT_CANDLE, 4)]),
        dict(id="dun_torches", name="Torches", level=84, xp=244,
             materials=[m(OAK_PLANK, 4), m(LIT_TORCH, 4)]),
        dict(id="dun_skull_torches", name="Skull torches", level=94, xp=246,
             materials=[m(OAK_PLANK, 4), m(LIT_TORCH, 4), m(SKULL, 4)]),
    ],
    "dun_decoration": [
        dict(id="decorative_blood", name="Decorative blood", level=72, xp=4,
             materials=[m(RED_DYE, 4)]),
        dict(id="decorative_pipe", name="Decorative pipe", level=83, xp=120,
             materials=[m(STEEL_BAR, 6)]),
        dict(id="hanging_skeleton", name="Hanging skeleton", level=94, xp=3,
             materials=[m(SKULL, 2), m(BONES, 6)]),
    ],
    "oub_floor": [
        dict(id="spikes_floor", name="Spikes", level=65, xp=623,
             materials=[m(STEEL_BAR, 20)], coins=50000),
        dict(id="tentacle_pool", name="Tentacle pool", level=71, xp=326,
             materials=[m(BUCKET_OF_WATER, 20)], coins=100000),
        dict(id="flame_pit", name="Flame pit", level=77, xp=357, materials=[], coins=125000,
             note="Also needs 20 tinderboxes"),
        dict(id="rocnar", name="Rocnar", level=83, xp=387, materials=[], coins=150000),
    ],
    "oub_prison": [
        dict(id="oak_cage", name="Oak cage", level=65, xp=640,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 2)]),
        dict(id="oak_and_steel_cage", name="Oak and steel cage", level=70, xp=800,
             materials=[m(OAK_PLANK, 10), m(STEEL_BAR, 10)]),
        dict(id="steel_cage", name="Steel cage", level=75, xp=400, materials=[m(STEEL_BAR, 20)]),
        dict(id="spiked_cage", name="Spiked cage", level=80, xp=500, materials=[m(STEEL_BAR, 25)]),
        dict(id="bone_cage", name="Bone cage", level=85, xp=603,
             materials=[m(OAK_PLANK, 10), m(BONES, 10)]),
    ],
    "oub_ladder": [
        dict(id="oak_ladder", name="Oak ladder", level=68, xp=300, materials=[m(OAK_PLANK, 5)]),
        dict(id="teak_ladder", name="Teak ladder", level=78, xp=450, materials=[m(TEAK_PLANK, 5)]),
        dict(id="mahogany_ladder", name="Mahogany ladder", level=88, xp=700,
             materials=[m(MAHOGANY_PLANK, 5)]),
    ],
    "treas_treasure": [
        dict(id="wooden_crate", name="Wooden crate", level=75, xp=143,
             materials=[m(PLANK, 5), m(NAILS, 5)], objectIds=[8148],
             note="Holds up to 10,000 coins"),
        dict(id="oak_chest_t", name="Oak chest", level=79, xp=340,
             materials=[m(OAK_PLANK, 5), m(STEEL_BAR, 2)], objectIds=[8149],
             note="Holds up to 20,000 coins"),
        dict(id="teak_chest_t", name="Teak chest", level=83, xp=530,
             materials=[m(TEAK_PLANK, 5), m(STEEL_BAR, 4)], objectIds=[8150],
             note="Holds up to 50,000 coins"),
        dict(id="mahogany_chest_t", name="Mahogany chest", level=87, xp=1000,
             materials=[m(MAHOGANY_PLANK, 5), m(GOLD_LEAF, 1)], objectIds=[8151],
             note="Holds up to 75,000 coins"),
        dict(id="magic_chest_t", name="Magic chest", level=91, xp=1500,
             materials=[m(MAGIC_STONE, 1)], note="Holds up to 100,000 coins"),
    ],
    "treas_monster": [
        dict(id="demon_monster", name="Demon", level=75, xp=707, materials=[], note="Bought outright rather than built from materials. The wiki does not publish its coin price, so it is not counted on the shopping list"),
        dict(id="kalphite_soldier", name="Kalphite soldier", level=80, xp=866, materials=[], note="Bought outright rather than built from materials. The wiki does not publish its coin price, so it is not counted on the shopping list"),
        dict(id="tok_xil", name="Tok-Xil", level=85, xp=2236, materials=[], note="Bought outright rather than built from materials. The wiki does not publish its coin price, so it is not counted on the shopping list"),
        dict(id="dagannoth_monster", name="Dagannoth", level=90, xp=2738, materials=[], note="Bought outright rather than built from materials. The wiki does not publish its coin price, so it is not counted on the shopping list"),
        dict(id="steel_dragon_monster", name="Steel dragon", level=95, xp=3162, materials=[], note="Bought outright rather than built from materials. The wiki does not publish its coin price, so it is not counted on the shopping list"),
        dict(id="rune_dragon_monster", name="Rune dragon", level=99, xp=5000, materials=[],
             note="Also needs Dragon Slayer II"),
    ],
    # --- League hall -------------------------------------------------------
    "lh_pedestal": [
        dict(id="trophy_pedestal", name="Trophy pedestal", level=27, xp=86,
             materials=[m(LIMESTONE_BRICK, 4), m(ROPE, 1), m(RED_DYE, 1)]),
        dict(id="ornate_trophy_pedestal", name="Ornate trophy pedestal", level=64, xp=2106,
             materials=[m(MARBLE_BLOCK, 3), m(GOLD_LEAF, 1), m(ROPE, 1), m(RED_DYE, 1)]),
    ],
    "lh_trophy_case": [
        dict(id="oak_trophy_case", name="Oak trophy case", level=36, xp=360,
             materials=[m(OAK_PLANK, 6)]),
        dict(id="mahogany_trophy_case", name="Mahogany trophy case", level=78, xp=1440,
             materials=[m(MAHOGANY_PLANK, 6), m(GOLD_LEAF, 2)]),
    ],
    "lh_banner": [
        dict(id="banner_stand", name="Banner stand", level=30, xp=40,
             materials=[m(LIMESTONE_BRICK, 2)]),
        dict(id="ornate_banner_stand", name="Ornate banner stand", level=66, xp=1300,
             materials=[m(MARBLE_BLOCK, 2), m(GOLD_LEAF, 1)]),
    ],
    "lh_outfit": [
        dict(id="oak_outfit_stand", name="Oak outfit stand", level=34, xp=240,
             materials=[m(OAK_PLANK, 4)]),
        dict(id="mahogany_outfit_stand", name="Mahogany outfit stand", level=74, xp=860,
             materials=[m(MAHOGANY_PLANK, 4), m(GOLD_LEAF, 1)]),
    ],
    "lh_statue": [
        dict(id="league_statue", name="League statue", level=32, xp=120,
             materials=[m(LIMESTONE_BRICK, 6)]),
        dict(id="ornate_league_statue", name="Ornate league statue", level=68, xp=3600,
             materials=[m(MARBLE_BLOCK, 6), m(GOLD_LEAF, 1)]),
    ],
    "lh_scroll": [
        dict(id="league_scroll", name="League accomplishments scroll", level=48, xp=310,
             materials=[m(PAPYRUS, 10), m(GOLD_LEAF, 1)]),
    ],
}

# ---------------------------------------------------------------------------
# Rooms. `objects` on a hotspot are the empty build hotspot object ids from the
# cache; `family` names the entry in FURNITURE holding what can go there.
# `planes`: 0 dungeon, 1 ground floor, 2 first floor.
# ---------------------------------------------------------------------------

GROUND_AND_UP = [1, 2]
OUTDOORS = [1]        # gardens are open to the sky, so they sit on the ground floor
BASEMENT = [0]

ROOMS = [
    dict(
        id="garden", name="Garden", level=1, cost=1000, planes=[1], colour="#4C7A3F", doors=["NORTH", "EAST", "SOUTH", "WEST"],
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
        id="parlour", name="Parlour", level=1, cost=1000, planes=GROUND_AND_UP, colour="#8B6F47", doors=["EAST", "SOUTH", "WEST"],
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
        id="kitchen", name="Kitchen", level=5, cost=5000, planes=GROUND_AND_UP, colour="#B07A3C", doors=["EAST", "SOUTH"],
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
        id="dining_room", name="Dining room", level=10, cost=5000, planes=GROUND_AND_UP, colour="#9C5B3C", doors=["EAST", "SOUTH", "WEST"],
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
        id="bedroom", name="Bedroom", level=20, cost=10000, planes=GROUND_AND_UP, colour="#6B5B95", doors=["EAST", "SOUTH"],
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
        colour="#3E6B8A", doors=["NORTH", "EAST", "SOUTH", "WEST"],
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
    dict(
        id="workshop", name="Workshop", level=15, cost=10000, planes=GROUND_AND_UP, colour="#6E6E6E",
        doors=["NORTH", "SOUTH"],
        note="Makes flatpacks, clockwork toys and heraldic items, and repairs armour",
        hotspots=[
            dict(id="workbench", name="Workbench space", objects=[15439], family="workshop_workbench"),
            dict(id="clockmaking", name="Clockmaking space", objects=[15441], family="workshop_clockmaking"),
            dict(id="tool", name="Tool space", objects=[15443, 15444, 15445, 15446, 15447],
                 family="workshop_tool"),
            dict(id="repair", name="Repair space", objects=[15448], family="workshop_repair"),
            dict(id="heraldry", name="Heraldry space", objects=[15450], family="workshop_heraldry"),
        ],
    ),
    dict(
        id="study", name="Study", level=40, cost=50000, planes=GROUND_AND_UP, colour="#4E7D8C",
        doors=["EAST", "SOUTH", "WEST"],
        note="Three doorways, so it works as a straight room or a corner room",
        hotspots=[
            dict(id="lectern", name="Lectern space", objects=[15420], family="study_lectern"),
            dict(id="globe", name="Globe space", objects=[15421], family="study_globe"),
            dict(id="crystal_ball", name="Crystal ball space", objects=[15422], family="study_crystal_ball"),
            dict(id="wall_chart", name="Wall chart space", objects=[15423], family="study_wall_chart"),
            dict(id="telescope", name="Telescope space", objects=[15424], family="study_telescope"),
            dict(id="bookcase", name="Bookcase space", objects=[15425], family="parlour_bookcase"),
        ],
    ),
    dict(
        id="chapel", name="Chapel", level=45, cost=50000, planes=GROUND_AND_UP, colour="#8C7BAE",
        doors=["EAST", "SOUTH"],
        note="A gilded altar with both burners lit gives 350% Prayer experience for bones",
        hotspots=[
            dict(id="icon", name="Icon space", objects=[15269], family="chapel_icon"),
            dict(id="altar", name="Altar space", objects=[15270], family="chapel_altar"),
            dict(id="lamp", name="Lamp space", objects=[15271], family="chapel_lamp"),
            dict(id="rug", name="Rug space", objects=[15272, 15273, 15274], family="parlour_rug"),
            dict(id="statue", name="Statue space", objects=[15275], family="chapel_statue"),
            dict(id="musical", name="Musical space", objects=[15276], family="chapel_musical"),
            dict(id="window", name="Window space",
                 objects=[13728, 13729, 13730, 13731, 13732, 13733, 27070, 37438, 37619, 40770,
                          56141, 56142, 60660],
                 family="chapel_window"),
        ],
    ),
    dict(
        id="portal_chamber", name="Portal chamber", level=50, cost=100000, planes=GROUND_AND_UP,
        colour="#5D5FA8", doors=["SOUTH"],
        note="Three portals, each aimed at one destination. The centrepiece is what aims them",
        hotspots=[
            dict(id="portal_1", name="Portal space 1", objects=[15406], family="portal_frame"),
            dict(id="portal_2", name="Portal space 2", objects=[15407], family="portal_frame"),
            dict(id="portal_3", name="Portal space 3", objects=[15408], family="portal_frame"),
            dict(id="centrepiece", name="Centrepiece space", objects=[15409],
                 family="portal_centrepiece"),
        ],
    ),
    dict(
        id="quest_hall", name="Hall (quest trophies)", level=35, cost=25000, planes=GROUND_AND_UP,
        colour="#7A5C99", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Also called the quest hall. A staircase here links floors",
        hotspots=[
            dict(id="stairs", name="Stair space", objects=[15387, 15388, 15389, 15390, 15391],
                 family="hall_stairs"),
            dict(id="portrait", name="Portrait space", objects=[15392], family="quest_portrait"),
            dict(id="landscape", name="Landscape space", objects=[15393], family="quest_landscape"),
            dict(id="guild_trophy", name="Guild trophy space", objects=[15394],
                 family="quest_guild_trophy"),
            dict(id="sword", name="Sword space", objects=[15395], family="quest_sword"),
            dict(id="map", name="Map space", objects=[15396], family="quest_map"),
            dict(id="bookcase", name="Bookcase space", objects=[15397], family="parlour_bookcase"),
        ],
    ),
    dict(
        id="costume_room", name="Costume room", level=42, cost=50000, planes=GROUND_AND_UP,
        colour="#A8577A", doors=["SOUTH"],
        note="Stores holiday items, treasure trail rewards, capes and armour sets out of your bank",
        hotspots=[
            dict(id="cape_rack", name="Cape rack space", objects=[18810], family="costume_cape_rack"),
            dict(id="magic_wardrobe", name="Magic wardrobe space", objects=[18811],
                 family="costume_wardrobe"),
            dict(id="toy_box", name="Toy box space", objects=[18812], family="costume_toy_box"),
            dict(id="treasure_chest", name="Treasure chest space", objects=[18813],
                 family="costume_treasure_chest"),
            dict(id="fancy_dress_box", name="Fancy dress box space", objects=[18814],
                 family="costume_fancy_dress"),
            dict(id="armour_case", name="Armour case space", objects=[18815],
                 family="costume_armour_case"),
        ],
    ),
    dict(
        id="achievement_gallery", name="Achievement gallery", level=80, cost=200000,
        planes=GROUND_AND_UP, colour="#B8892E", doors=["NORTH", "SOUTH"],
        note="Holds the jewellery box and the spellbook altar, two of the most useful things in a house",
        hotspots=[
            dict(id="altar", name="Altar space", objects=[29140], family="achv_altar"),
            dict(id="adventure_log", name="Adventure log space", objects=[29141], family="achv_log"),
            dict(id="jewellery_box", name="Jewellery box space", objects=[29142],
                 family="achv_jewellery"),
            dict(id="boss_lair", name="Boss lair space", objects=[29143], family="achv_lair"),
            dict(id="display", name="Display space", objects=[29144], family="achv_display"),
            dict(id="quest_list", name="Quest list space", objects=[29145], family="achv_questlist"),
        ],
    ),
    dict(
        id="portal_nexus", name="Portal nexus", level=72, cost=200000, planes=GROUND_AND_UP,
        colour="#4A4AA0", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="One portal that covers every destination at once. Only one per house",
        hotspots=[
            dict(id="nexus", name="Portal nexus space", objects=[33346], family="nexus"),
            dict(id="rug", name="Rug space", objects=[33347, 33349, 33350], family="parlour_rug"),
            dict(id="curtain", name="Curtain space", objects=[33351], family="parlour_curtain"),
            dict(id="amulet_1", name="Amulet space 1", objects=[33352], family="nexus_amulet"),
            dict(id="amulet_2", name="Amulet space 2", objects=[33353], family="nexus_amulet"),
        ],
    ),
    dict(
        id="superior_garden", name="Superior garden", level=65, cost=75000, planes=OUTDOORS,
        colour="#3F8A5C", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Holds the rejuvenation pool and a fairy ring or spirit tree",
        hotspots=[
            dict(id="teleport", name="Teleport space", objects=[29120], family="sg_teleport"),
            dict(id="topiary", name="Topiary space", objects=[29121], family="sg_topiary"),
            dict(id="pool", name="Pool space", objects=[29122], family="sg_pool"),
            dict(id="theme", name="Theme space",
                 objects=[29123, 29124, 29125, 29126, 29127, 29128, 29129, 29130], family="sg_theme"),
            dict(id="fence", name="Fence space", objects=[29131, 29132, 29133], family="sg_fence"),
            dict(id="seating_1", name="Seating space 1", objects=[29136, 29137], family="sg_seating"),
            dict(id="seating_2", name="Seating space 2", objects=[29138, 29139], family="sg_seating"),
        ],
    ),
    dict(
        id="combat_room", name="Combat room", level=32, cost=25000, planes=GROUND_AND_UP,
        colour="#A34B3C", doors=["EAST", "SOUTH", "WEST"],
        hotspots=[
            dict(id="combat_ring", name="Combat ring space",
                 objects=[15277, 15278, 15279, 15280, 15281, 15282, 15283, 15284, 15285, 15286,
                          15287, 15288, 15289, 15290, 15291, 15292, 15293, 15294, 15295],
                 family="combat_ring"),
            dict(id="storage", name="Storage space", objects=[15296], family="combat_storage"),
            dict(id="decoration", name="Decoration space", objects=[15297],
                 family="dining_decoration"),
            dict(id="combat_dummy", name="Combat dummy space", objects=[29335],
                 family="combat_dummy"),
        ],
    ),
    dict(
        id="games_room", name="Games room", level=30, cost=25000, planes=GROUND_AND_UP,
        colour="#C08A2E", doors=["EAST", "SOUTH", "WEST"],
        hotspots=[
            dict(id="game", name="Game space", objects=[15342], family="games_game"),
            dict(id="prize_chest", name="Prize chest space", objects=[15343], family="games_prize"),
            dict(id="stone", name="Stone space", objects=[15344], family="games_stone"),
            dict(id="elemental_balance", name="Elemental balance space", objects=[15345],
                 family="games_elemental"),
            dict(id="ranging_game", name="Ranging game space", objects=[15346],
                 family="games_ranging"),
        ],
    ),
    dict(
        id="formal_garden", name="Formal garden", level=55, cost=75000, planes=OUTDOORS,
        colour="#4F9E63", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Can hold the exit portal instead of a plain garden",
        hotspots=[
            dict(id="centrepiece", name="Centrepiece space", objects=[15368],
                 family="fg_centrepiece"),
            dict(id="fencing", name="Fencing space", objects=[15369], family="fg_fencing"),
            dict(id="hedging", name="Hedging space", objects=[15370, 15371, 15372],
                 family="fg_hedging"),
            dict(id="big_plant_1", name="Big plant space 1", objects=[15373], family="fg_plant_set_1"),
            dict(id="big_plant_2", name="Big plant space 2", objects=[15374], family="fg_plant_set_2"),
            dict(id="small_plant_1", name="Small plant space 1", objects=[15375],
                 family="fg_plant_set_1"),
            dict(id="small_plant_2", name="Small plant space 2", objects=[15376],
                 family="fg_plant_set_2"),
        ],
    ),
    dict(
        id="throne_room", name="Throne room", level=60, cost=150000, planes=GROUND_AND_UP,
        colour="#9B4F8C", doors=["SOUTH"],
        note="The lever and trapdoor drop guests into an oubliette built directly below",
        hotspots=[
            dict(id="throne", name="Throne space", objects=[15426], family="throne_throne"),
            dict(id="floor", name="Floor space",
                 objects=[15427, 15428, 15429, 15430, 15431, 15432, 27071], family="throne_floor"),
            dict(id="decoration", name="Decoration space", objects=[15433, 15434],
                 family="throne_decoration"),
            dict(id="lever", name="Lever space", objects=[15435], family="throne_lever"),
            dict(id="seating_1", name="Seating space 1", objects=[15436], family="dining_seating"),
            dict(id="seating_2", name="Seating space 2", objects=[15437], family="dining_seating"),
            dict(id="trapdoor", name="Trapdoor space", objects=[15438], family="throne_trapdoor"),
        ],
    ),
    dict(
        id="menagerie", name="Menagerie", level=37, cost=30000, planes=GROUND_AND_UP,
        colour="#6FA83C", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Houses your pets. The habitat hotspot only exists in the outdoor version",
        hotspots=[
            dict(id="pet_house", name="Pet house space", objects=[26296], family="men_pethouse"),
            dict(id="habitat", name="Habitat space",
                 objects=[26833, 26839, 26845, 26851], family="men_habitat"),
            dict(id="scratching_post", name="Scratching post space", objects=[26857],
                 family="men_scratch"),
            dict(id="arena", name="Arena space", objects=[26861, 26865], family="men_arena"),
            dict(id="pet_list", name="Pet list space", objects=[26867], family="men_petlist"),
            dict(id="pet_feeder", name="Pet feeder space", objects=[26869], family="men_feeder"),
        ],
    ),
    dict(
        id="oubliette", name="Oubliette", level=65, cost=150000, planes=BASEMENT,
        colour="#6B4A3A", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Built in the basement, directly below a throne room",
        hotspots=[
            dict(id="floor", name="Floor space", objects=[15347, 15348, 15349, 15350, 15351],
                 family="oub_floor"),
            dict(id="prison", name="Prison space", objects=[15352, 15353], family="oub_prison"),
            dict(id="guard", name="Guard space", objects=[15354], family="dun_guard"),
            dict(id="lighting", name="Lighting space", objects=[15355], family="dun_lighting"),
            dict(id="ladder", name="Ladder space", objects=[15356], family="oub_ladder"),
            dict(id="door", name="Door space", objects=[15357, 15358, 15359, 15360],
                 family="dun_door"),
        ],
    ),
    dict(
        id="dungeon_corridor", name="Dungeon corridor", level=70, cost=7500, planes=BASEMENT,
        colour="#57504A", doors=["EAST", "WEST"],
        note="A straight length of dungeon. Corridors and junctions share the same fittings, so "
             "the plugin cannot always tell one from the other when reading your house",
        hotspots=[
            dict(id="guard", name="Guard space", objects=[15323], family="dun_guard"),
            dict(id="trap", name="Trap space", objects=[15324, 15325], family="dun_trap"),
            dict(id="door", name="Door space", objects=[15326, 15327, 15328, 15329],
                 family="dun_door"),
            dict(id="lighting", name="Lighting space", objects=[15330], family="dun_lighting"),
            dict(id="decoration", name="Decoration space", objects=[15331], family="dun_decoration"),
        ],
    ),
    dict(
        id="dungeon_junction", name="Dungeon junction", level=70, cost=7500, planes=BASEMENT,
        colour="#5E574F", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="A dungeon crossroads. Shares its fittings with the corridor",
        hotspots=[
            dict(id="guard", name="Guard space", objects=[15323], family="dun_guard"),
            dict(id="trap", name="Trap space", objects=[15324, 15325], family="dun_trap"),
            dict(id="door", name="Door space", objects=[15326, 15327, 15328, 15329],
                 family="dun_door"),
            dict(id="lighting", name="Lighting space", objects=[15330], family="dun_lighting"),
            dict(id="decoration", name="Decoration space", objects=[15331], family="dun_decoration"),
        ],
    ),
    dict(
        id="dungeon_stairs", name="Dungeon stairs", level=70, cost=7500, planes=BASEMENT,
        colour="#6A6157", doors=["NORTH", "EAST", "SOUTH", "WEST"],
        note="Where the dungeon meets the floor above",
        hotspots=[
            dict(id="stairs", name="Rug and stair space", objects=[15332, 15333, 15334, 15335],
                 family="hall_stairs"),
            dict(id="guard_1", name="Guard space 1", objects=[15336], family="dun_guard"),
            dict(id="guard_2", name="Guard space 2", objects=[15337], family="dun_guard"),
            dict(id="door", name="Door space", objects=[15338, 15339], family="dun_door"),
            dict(id="lighting", name="Lighting space", objects=[15340], family="dun_lighting"),
            dict(id="decoration", name="Decoration space", objects=[15341], family="dun_decoration"),
        ],
    ),
    dict(
        id="treasure_room", name="Treasure room", level=75, cost=250000, planes=BASEMENT,
        colour="#B08A3A", doors=["SOUTH"],
        note="The deepest room in the dungeon, and the most expensive in the house",
        hotspots=[
            dict(id="treasure", name="Treasure space", objects=[15256], family="treas_treasure"),
            dict(id="monster", name="Monster space", objects=[15257], family="treas_monster"),
            dict(id="decoration", name="Decoration space", objects=[15259],
                 family="dun_decoration"),
        ],
    ),
    dict(
        id="league_hall", name="League hall", level=27, cost=15000, planes=GROUND_AND_UP,
        colour="#3E7F8A", doors=["EAST", "SOUTH", "WEST"],
        note="Displays league trophies and rewards",
        hotspots=[
            dict(id="pedestal_1", name="Pedestal space 1", objects=[41024], family="lh_pedestal"),
            dict(id="pedestal_2", name="Pedestal space 2", objects=[41025], family="lh_pedestal"),
            dict(id="pedestal_3", name="Pedestal space 3", objects=[41026], family="lh_pedestal"),
            dict(id="trophy_case", name="Trophy case space", objects=[41027],
                 family="lh_trophy_case"),
            dict(id="banner_stand", name="Banner stand space", objects=[41028], family="lh_banner"),
            dict(id="outfit_stand", name="Outfit stand space", objects=[41029], family="lh_outfit"),
            dict(id="statue", name="Statue space", objects=[41030], family="lh_statue"),
            dict(id="rug", name="Rug space", objects=[41031, 41032, 41033], family="parlour_rug"),
            dict(id="scroll", name="Accomplishment scroll space", objects=[41034],
                 family="lh_scroll"),
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
    if option.get("coins"):
        entry["coins"] = option["coins"]
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
