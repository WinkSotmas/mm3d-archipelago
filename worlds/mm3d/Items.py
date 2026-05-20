from BaseClasses import Item, ItemClassification

MM3D_BASE_ID = 0xAB3D_0000  # Unique base ID for MM3D items — change if it conflicts


class MM3DItem(Item):
    game = "Majora's Mask 3D"


# Classification shorthands
prog   = ItemClassification.progression
useful = ItemClassification.useful
filler = ItemClassification.filler
trap   = ItemClassification.trap

# (name, classification, id_offset)
# id_offset is added to MM3D_BASE_ID to produce the full item ID.
# Items marked with offset None are events (no ID needed).
MM3D_ITEM_TABLE: dict[str, tuple[ItemClassification, int | None]] = {
    # ── Masks (progression / useful) ───────────────────────────────────────
    "Deku Mask":          (prog,   0x00),
    "Goron Mask":         (prog,   0x01),
    "Zora Mask":          (prog,   0x02),
    "Fierce Deity Mask":  (useful, 0x03),
    "Postman's Hat":      (useful, 0x04),
    "All-Night Mask":     (useful, 0x05),
    "Blast Mask":         (useful, 0x06),
    "Stone Mask":         (useful, 0x07),
    "Great Fairy Mask":   (useful, 0x08),
    "Bremen Mask":        (prog,   0x09),
    "Bunny Hood":         (useful, 0x0A),
    "Don Gero's Mask":    (prog,   0x0B),
    "Mask of Scents":     (useful, 0x0C),
    "Romani's Mask":      (useful, 0x0D),
    "Troupe Leader Mask": (useful, 0x0E),
    "Kafei's Mask":       (prog,   0x0F),
    "Couple's Mask":      (useful, 0x10),
    "Mask of Truth":      (useful, 0x11),
    "Kamaro's Mask":      (useful, 0x12),
    "Gibdo Mask":         (prog,   0x13),
    "Garo's Mask":        (prog,   0x14),
    "Captain's Hat":      (prog,   0x15),
    "Giant's Mask":       (prog,   0x16),
    "Keaton Mask":        (useful, 0x17),
    "Circus Leader's Mask": (useful, 0x18),

    # ── Key items ──────────────────────────────────────────────────────────
    "Ocarina of Time":    (prog,   0x20),
    "Bomb Bag":           (prog,   0x21),
    "Bow":                (prog,   0x22),
    "Fire Arrows":        (prog,   0x23),
    "Ice Arrows":         (prog,   0x24),
    "Light Arrows":       (prog,   0x25),
    "Hookshot":           (prog,   0x26),
    "Lens of Truth":      (prog,   0x27),
    "Magic Beans":        (prog,   0x28),
    "Powder Keg":         (prog,   0x29),
    "Pictograph Box":     (useful, 0x2A),
    "Bottles":            (prog,   0x2B),  # treated as a single progressive item
    "Sword Upgrade":      (prog,   0x2C),  # progressive: Kokiri → Razor → Gilded

    # ── Songs ──────────────────────────────────────────────────────────────
    "Sonata of Awakening":   (prog, 0x30),
    "Goron Lullaby":         (prog, 0x31),
    "New Wave Bossa Nova":   (prog, 0x32),
    "Elegy of Emptiness":    (prog, 0x33),
    "Oath to Order":         (prog, 0x34),
    "Song of Time":          (prog, 0x35),
    "Song of Healing":       (prog, 0x36),
    "Epona's Song":          (useful, 0x37),
    "Song of Soaring":       (useful, 0x38),
    "Song of Storms":        (prog, 0x39),
    "Scarecrow's Song":      (useful, 0x3A),

    # ── Dungeon items ──────────────────────────────────────────────────────
    "Woodfall Small Key":      (prog,   0x40),
    "Snowhead Small Key":      (prog,   0x41),
    "Great Bay Small Key":     (prog,   0x42),
    "Stone Tower Small Key":   (prog,   0x43),
    "Woodfall Boss Key":       (prog,   0x44),
    "Snowhead Boss Key":       (prog,   0x45),
    "Great Bay Boss Key":      (prog,   0x46),
    "Stone Tower Boss Key":    (prog,   0x47),
    "Woodfall Map":            (useful, 0x48),
    "Snowhead Map":            (useful, 0x49),
    "Great Bay Map":           (useful, 0x4A),
    "Stone Tower Map":         (useful, 0x4B),
    "Woodfall Compass":        (useful, 0x4C),
    "Snowhead Compass":        (useful, 0x4D),
    "Great Bay Compass":       (useful, 0x4E),
    "Stone Tower Compass":     (useful, 0x4F),

    # ── Filler / consumables ───────────────────────────────────────────────
    "Rupees (5)":    (filler, 0x60),
    "Rupees (20)":   (filler, 0x61),
    "Rupees (50)":   (filler, 0x62),
    "Rupees (200)":  (filler, 0x63),
    "Magic Jar (S)": (filler, 0x64),
    "Magic Jar (L)": (filler, 0x65),
    "Heart Piece":   (useful, 0x66),
    "Heart Container": (useful, 0x67),

    # ── Event / victory (no ID) ────────────────────────────────────────────
    "Victory":       (prog, None),
}


def get_item_id(name: str) -> int | None:
    """Return the full AP item ID for a given item name, or None for events."""
    classification, offset = MM3D_ITEM_TABLE[name]
    if offset is None:
        return None
    return MM3D_BASE_ID + offset


def create_item(name: str, player: int) -> MM3DItem:
    classification, offset = MM3D_ITEM_TABLE[name]
    return MM3DItem(name, classification, get_item_id(name), player)


# Items that are always progression-critical and must not be filler-replaced
PROGRESSION_ITEMS = {name for name, (cls, _) in MM3D_ITEM_TABLE.items() if cls == prog}

# Filler pool — used to pad the item pool when needed
FILLER_ITEMS = [name for name, (cls, _) in MM3D_ITEM_TABLE.items() if cls == filler]
