#!/usr/bin/env python3
"""Checks rooms.json for the mistakes that break house detection.

Mirrors src/test/java/com/pohtemplates/data/PohDataTest.java so a bad
regeneration is caught before it reaches a build.

Run:  python3 tools/validate_data.py
"""
import collections
import json
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "src", "main", "resources", "com", "pohtemplates", "rooms.json")


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    errors, warnings = [], []

    item_ids = {i["itemId"] for i in data["items"]}
    valid_doors = {"NORTH", "EAST", "SOUTH", "WEST"}
    hotspot_objects, furniture_objects = {}, {}
    room_ids = set()

    for room in data["rooms"]:
        if room["id"] in room_ids:
            errors.append("duplicate room id %s" % room["id"])
        room_ids.add(room["id"])

        if not 1 <= room["level"] <= 99:
            errors.append("%s has level %s" % (room["id"], room["level"]))
        if not room["planes"]:
            errors.append("%s has no planes" % room["id"])
        if not room["hotspots"]:
            errors.append("%s has no hotspots" % room["id"])

        doors = room.get("doors")
        if not doors:
            warnings.append("%s has no door layout, so it cannot be checked for connectivity"
                            % room["id"])
        else:
            for door in doors:
                if door not in valid_doors:
                    errors.append("%s has an unknown door side %r" % (room["id"], door))
            if len(set(doors)) != len(doors):
                errors.append("%s lists the same door side twice" % room["id"])

        hotspot_ids = set()
        for hotspot in room["hotspots"]:
            key = "%s/%s" % (room["id"], hotspot["id"])
            if hotspot["id"] in hotspot_ids:
                errors.append("duplicate hotspot %s" % key)
            hotspot_ids.add(hotspot["id"])

            if not hotspot.get("objectIds"):
                errors.append("%s has no object ids" % key)
            if not hotspot.get("options"):
                errors.append("%s has nothing to build" % key)

            for object_id in hotspot.get("objectIds", []):
                hotspot_objects.setdefault(object_id, []).append(key)

            option_ids, previous_level = set(), 0
            for option in hotspot.get("options", []):
                if option["id"] in option_ids:
                    errors.append("duplicate furniture %s in %s" % (option["id"], key))
                option_ids.add(option["id"])

                if not 1 <= option["level"] <= 99:
                    errors.append("%s has level %s" % (option["id"], option["level"]))
                if option["xp"] < 0:
                    errors.append("%s has negative xp" % option["id"])
                if option.get("coins", 0) < 0:
                    errors.append("%s has a negative coin cost" % option["id"])
                if not option.get("materials") and not option.get("coins") and not option.get("note"):
                    warnings.append("%s costs nothing and explains nothing" % option["id"])
                if option["level"] < previous_level:
                    warnings.append("%s: %s (level %d) is listed after level %d"
                                    % (key, option["id"], option["level"], previous_level))
                previous_level = option["level"]

                for material in option.get("materials", []):
                    if material["quantity"] <= 0:
                        errors.append("%s asks for %s of an item"
                                      % (option["id"], material["quantity"]))
                    if material["itemId"] not in item_ids:
                        errors.append("%s uses item %s, which has no entry in items"
                                      % (option["id"], material["itemId"]))

                for object_id in option.get("objectIds", []):
                    furniture_objects.setdefault(object_id, []).append(
                        "%s/%s" % (key, option["id"]))

    for object_id in set(hotspot_objects) & set(furniture_objects):
        errors.append("object %s is both an empty hotspot (%s) and built furniture (%s)"
                      % (object_id, hotspot_objects[object_id], furniture_objects[object_id]))

    for object_id, uses in hotspot_objects.items():
        rooms = collections.Counter(use.split("/")[0] for use in uses)
        for room_id, count in rooms.items():
            if count > 1:
                errors.append("object %s means %d different hotspots inside %s: %s"
                              % (object_id, count, room_id, uses))

    hotspots = sum(len(r["hotspots"]) for r in data["rooms"])
    options = sum(len(h["options"]) for r in data["rooms"] for h in r["hotspots"])
    print("%d rooms, %d hotspots, %d furniture options, %d items"
          % (len(data["rooms"]), hotspots, options, len(data["items"])))
    print("%d hotspot object ids, %d furniture object ids"
          % (len(hotspot_objects), len(furniture_objects)))

    for warning in warnings:
        print("WARNING: %s" % warning)
    for error in errors:
        print("ERROR: %s" % error)

    print("RESULT: %s" % ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
