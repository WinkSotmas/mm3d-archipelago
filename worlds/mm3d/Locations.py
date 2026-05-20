from BaseClasses import Location
from .Items import MM3D_BASE_ID

# Location IDs start after item IDs.  Give locations their own offset range.
MM3D_LOC_BASE_ID = MM3D_BASE_ID + 0x1000


class MM3DLocation(Location):
    game = "Majora's Mask 3D"


# (region_name, id_offset)
# region_name must match a key in Regions.MM3D_REGIONS.
MM3D_LOCATION_TABLE: dict[str, tuple[str, int]] = {
    # ── Clock Town ─────────────────────────────────────────────────────────
    "Clock Town - Song of Healing":          ("Clock Town", 0x000),
    "Clock Town - Deku Playground (Night 1)": ("Clock Town", 0x001),
    "Clock Town - Deku Playground (Night 2)": ("Clock Town", 0x002),
    "Clock Town - Deku Playground (Night 3)": ("Clock Town", 0x003),
    "Clock Town - Postman's Hat":            ("Clock Town", 0x004),
    "Clock Town - Mayor's Deed":             ("Clock Town", 0x005),
    "Clock Town - Kafei's Letter":           ("Clock Town", 0x006),
    "Clock Town - Couple's Mask Reward":     ("Clock Town", 0x007),
    "Clock Town - Lottery Shop":             ("Clock Town", 0x008),
    "Clock Town - Bomb Shop (Day 1)":        ("Clock Town", 0x009),
    "Clock Town - Bomb Shop (Day 3)":        ("Clock Town", 0x00A),
    "Clock Town - Chest (Treasure Game)":    ("Clock Town", 0x00B),
    "Clock Town - Peahat Grotto Chest":      ("Clock Town", 0x00C),
    "Clock Town - Great Fairy Reward":       ("Clock Town", 0x00D),

    # ── Woodfall / Southern Swamp ──────────────────────────────────────────
    "Southern Swamp - Koume's Reward":       ("Southern Swamp", 0x010),
    "Southern Swamp - Pictograph Contest":   ("Southern Swamp", 0x011),
    "Woodfall Temple - Map Chest":           ("Woodfall Temple", 0x012),
    "Woodfall Temple - Compass Chest":       ("Woodfall Temple", 0x013),
    "Woodfall Temple - Small Key Chest":     ("Woodfall Temple", 0x014),
    "Woodfall Temple - Boss Key Chest":      ("Woodfall Temple", 0x015),
    "Woodfall Temple - Pre-Boss Chest":      ("Woodfall Temple", 0x016),
    "Woodfall Temple - Odolwa Heart Container": ("Woodfall Temple", 0x017),

    # ── Snowhead / Mountain Village ────────────────────────────────────────
    "Mountain Village - Blacksmith's Sword": ("Mountain Village", 0x020),
    "Mountain Village - Goron Graveyard":    ("Mountain Village", 0x021),
    "Snowhead Temple - Map Chest":           ("Snowhead Temple", 0x022),
    "Snowhead Temple - Compass Chest":       ("Snowhead Temple", 0x023),
    "Snowhead Temple - Small Key Chest 1":   ("Snowhead Temple", 0x024),
    "Snowhead Temple - Small Key Chest 2":   ("Snowhead Temple", 0x025),
    "Snowhead Temple - Small Key Chest 3":   ("Snowhead Temple", 0x026),
    "Snowhead Temple - Boss Key Chest":      ("Snowhead Temple", 0x027),
    "Snowhead Temple - Goht Heart Container": ("Snowhead Temple", 0x028),

    # ── Great Bay ──────────────────────────────────────────────────────────
    "Great Bay Coast - Mikau's Reward":      ("Great Bay", 0x030),
    "Great Bay Coast - Fisherman's Game":    ("Great Bay", 0x031),
    "Great Bay Temple - Map Chest":          ("Great Bay Temple", 0x032),
    "Great Bay Temple - Compass Chest":      ("Great Bay Temple", 0x033),
    "Great Bay Temple - Small Key Chest":    ("Great Bay Temple", 0x034),
    "Great Bay Temple - Boss Key Chest":     ("Great Bay Temple", 0x035),
    "Great Bay Temple - Gyorg Heart Container": ("Great Bay Temple", 0x036),

    # ── Ikana / Stone Tower ────────────────────────────────────────────────
    "Ikana Canyon - Music Box House":        ("Ikana Canyon", 0x040),
    "Ikana Canyon - Sharp's Curse Reward":   ("Ikana Canyon", 0x041),
    "Stone Tower Temple - Map Chest":        ("Stone Tower Temple", 0x042),
    "Stone Tower Temple - Compass Chest":    ("Stone Tower Temple", 0x043),
    "Stone Tower Temple - Small Key Chest 1": ("Stone Tower Temple", 0x044),
    "Stone Tower Temple - Small Key Chest 2": ("Stone Tower Temple", 0x045),
    "Stone Tower Temple - Small Key Chest 3": ("Stone Tower Temple", 0x046),
    "Stone Tower Temple - Boss Key Chest":   ("Stone Tower Temple", 0x047),
    "Stone Tower Temple - Twinmold Heart Container": ("Stone Tower Temple", 0x048),

    # ── Giants / Ending ────────────────────────────────────────────────────
    "Moon - Defeat Majora":                  ("Moon", 0x050),
}


def get_location_id(name: str) -> int:
    _, offset = MM3D_LOCATION_TABLE[name]
    return MM3D_LOC_BASE_ID + offset


# Convenience lookup: region → list of location names
def locations_by_region() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for loc_name, (region, _) in MM3D_LOCATION_TABLE.items():
        result.setdefault(region, []).append(loc_name)
    return result
