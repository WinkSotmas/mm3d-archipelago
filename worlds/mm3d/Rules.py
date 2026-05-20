"""
Access rules for MM3D locations and region transitions.

Rules are expressed as lambda functions over CollectionState.
Each helper returns True if the player currently has the required items.

NOTE: This is a first-pass logic skeleton.  MM3D logic is complex due to the
3-day cycle.  Cycle-sensitive checks (e.g. items only available on specific
days or nights) are marked with TODO comments for future refinement.
"""

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule, add_rule


# ── Helper predicates ────────────────────────────────────────────────────────

def has(state: CollectionState, player: int, *items: str) -> bool:
    """True if the player has ALL of the given items."""
    return all(state.has(item, player) for item in items)

def has_any(state: CollectionState, player: int, *items: str) -> bool:
    """True if the player has AT LEAST ONE of the given items."""
    return any(state.has(item, player) for item in items)

def can_access_deku(state: CollectionState, player: int) -> bool:
    return state.has("Deku Mask", player)

def can_access_goron(state: CollectionState, player: int) -> bool:
    return state.has("Goron Mask", player)

def can_access_zora(state: CollectionState, player: int) -> bool:
    return state.has("Zora Mask", player)

def can_swim(state: CollectionState, player: int) -> bool:
    return can_access_zora(state, player)

def can_blast(state: CollectionState, player: int) -> bool:
    """Any source of explosions."""
    return has_any(state, player, "Bomb Bag", "Blast Mask", "Powder Keg")

def can_shoot(state: CollectionState, player: int) -> bool:
    return state.has("Bow", player)

def has_hookshot(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)

def can_use_lens(state: CollectionState, player: int) -> bool:
    return state.has("Lens of Truth", player)

def has_song_of_time(state: CollectionState, player: int) -> bool:
    return has(state, player, "Ocarina of Time", "Song of Time")

# Boss remains — needed to open the Moon
def has_odolwa(state: CollectionState, player: int) -> bool:
    return state.has("Odolwa's Remains", player)   # placed by Victory event

def has_goht(state: CollectionState, player: int) -> bool:
    return state.has("Goht's Remains", player)

def has_gyorg(state: CollectionState, player: int) -> bool:
    return state.has("Gyorg's Remains", player)

def has_twinmold(state: CollectionState, player: int) -> bool:
    return state.has("Twinmold's Remains", player)

def has_all_remains(state: CollectionState, player: int) -> bool:
    return (has_odolwa(state, player) and has_goht(state, player)
            and has_gyorg(state, player) and has_twinmold(state, player))


# ── Region entrance rules ────────────────────────────────────────────────────

def set_entrance_rules(world: MultiWorld, player: int) -> None:
    # Clock Town → Southern Swamp: need Deku Mask to traverse Deku Forest region
    set_rule(world.get_entrance("Clock Town -> Southern Swamp", player),
             lambda state: can_access_deku(state, player))

    # Southern Swamp → Woodfall Temple
    set_rule(world.get_entrance("Southern Swamp -> Woodfall Temple", player),
             lambda state: (can_access_deku(state, player)
                            and state.has("Sonata of Awakening", player)))

    # Clock Town → Mountain Village: Goron or explosives to navigate Snowhead region
    set_rule(world.get_entrance("Clock Town -> Mountain Village", player),
             lambda state: can_access_goron(state, player))

    # Mountain Village → Snowhead Temple
    set_rule(world.get_entrance("Mountain Village -> Snowhead Temple", player),
             lambda state: (can_access_goron(state, player)
                            and state.has("Goron Lullaby", player)))

    # Clock Town → Great Bay: Zora to access bay properly
    set_rule(world.get_entrance("Clock Town -> Great Bay", player),
             lambda state: can_swim(state, player))

    # Great Bay → Great Bay Temple
    set_rule(world.get_entrance("Great Bay -> Great Bay Temple", player),
             lambda state: (can_swim(state, player)
                            and state.has("New Wave Bossa Nova", player)))

    # Clock Town → Ikana Canyon: Lens of Truth and Epona's Song (or hookshot for some paths)
    set_rule(world.get_entrance("Clock Town -> Ikana Canyon", player),
             lambda state: can_use_lens(state, player))

    # Ikana Canyon → Stone Tower Temple: Elegy of Emptiness + Zora + Deku + Goron
    set_rule(world.get_entrance("Ikana Canyon -> Stone Tower Temple", player),
             lambda state: (state.has("Elegy of Emptiness", player)
                            and can_access_deku(state, player)
                            and can_access_goron(state, player)
                            and can_access_zora(state, player)))

    # Clock Town → Moon: all four boss remains + Oath to Order
    set_rule(world.get_entrance("Clock Town -> Moon", player),
             lambda state: (has_all_remains(state, player)
                            and state.has("Oath to Order", player)))


# ── Location rules ────────────────────────────────────────────────────────────

def set_location_rules(world: MultiWorld, player: int) -> None:
    # ── Clock Town ──────────────────────────────────────────────────────────
    # Song of Healing is always accessible (given at game start)
    # Postman's Hat requires Kafei's Mask side quest
    set_rule(world.get_location("Clock Town - Postman's Hat", player),
             lambda state: state.has("Kafei's Mask", player))

    set_rule(world.get_location("Clock Town - Mayor's Deed", player),
             lambda state: (state.has("Kafei's Mask", player)
                            and state.has("Bremen Mask", player)))  # TODO: verify

    set_rule(world.get_location("Clock Town - Couple's Mask Reward", player),
             lambda state: state.has("Kafei's Mask", player))

    set_rule(world.get_location("Clock Town - Great Fairy Reward", player),
             lambda state: state.has("Stray Fairy (Clock Town)", player))  # placeholder

    set_rule(world.get_location("Clock Town - Bomb Shop (Day 3)", player),
             lambda state: state.has("Bomb Bag", player))

    # ── Woodfall Temple ─────────────────────────────────────────────────────
    set_rule(world.get_location("Woodfall Temple - Small Key Chest", player),
             lambda state: (can_access_deku(state, player)
                            and state.has("Woodfall Small Key", player)))

    set_rule(world.get_location("Woodfall Temple - Boss Key Chest", player),
             lambda state: (can_access_deku(state, player)
                            and state.has("Woodfall Small Key", player)))

    set_rule(world.get_location("Woodfall Temple - Pre-Boss Chest", player),
             lambda state: state.has("Woodfall Boss Key", player))

    set_rule(world.get_location("Woodfall Temple - Odolwa Heart Container", player),
             lambda state: state.has("Woodfall Boss Key", player))

    # ── Snowhead Temple ─────────────────────────────────────────────────────
    set_rule(world.get_location("Snowhead Temple - Small Key Chest 2", player),
             lambda state: state.has("Snowhead Small Key", player))

    set_rule(world.get_location("Snowhead Temple - Small Key Chest 3", player),
             lambda state: state.count("Snowhead Small Key", player) >= 2)

    set_rule(world.get_location("Snowhead Temple - Boss Key Chest", player),
             lambda state: (can_access_goron(state, player)
                            and state.count("Snowhead Small Key", player) >= 3))

    set_rule(world.get_location("Snowhead Temple - Goht Heart Container", player),
             lambda state: state.has("Snowhead Boss Key", player))

    # ── Great Bay Temple ────────────────────────────────────────────────────
    set_rule(world.get_location("Great Bay Temple - Small Key Chest", player),
             lambda state: (can_swim(state, player)
                            and can_shoot(state, player)))

    set_rule(world.get_location("Great Bay Temple - Boss Key Chest", player),
             lambda state: (can_swim(state, player)
                            and state.has("Great Bay Small Key", player)))

    set_rule(world.get_location("Great Bay Temple - Gyorg Heart Container", player),
             lambda state: state.has("Great Bay Boss Key", player))

    # ── Stone Tower Temple ──────────────────────────────────────────────────
    set_rule(world.get_location("Stone Tower Temple - Small Key Chest 2", player),
             lambda state: state.has("Stone Tower Small Key", player))

    set_rule(world.get_location("Stone Tower Temple - Small Key Chest 3", player),
             lambda state: state.count("Stone Tower Small Key", player) >= 2)

    set_rule(world.get_location("Stone Tower Temple - Boss Key Chest", player),
             lambda state: (can_use_lens(state, player)
                            and state.count("Stone Tower Small Key", player) >= 3
                            and state.has("Light Arrows", player)))

    set_rule(world.get_location("Stone Tower Temple - Twinmold Heart Container", player),
             lambda state: (state.has("Stone Tower Boss Key", player)
                            and state.has("Giant's Mask", player)))

    # ── Ikana ───────────────────────────────────────────────────────────────
    set_rule(world.get_location("Ikana Canyon - Music Box House", player),
             lambda state: state.has("Gibdo Mask", player))

    set_rule(world.get_location("Ikana Canyon - Sharp's Curse Reward", player),
             lambda state: (state.has("Song of Storms", player)
                            and state.has("Ocarina of Time", player)))

    # ── Moon ────────────────────────────────────────────────────────────────
    # Victory requires defeating Majora — gate this on all remains + Oath
    set_rule(world.get_location("Moon - Defeat Majora", player),
             lambda state: has_all_remains(state, player))


# ── Entry point ───────────────────────────────────────────────────────────────

def set_rules(world: MultiWorld, player: int) -> None:
    set_entrance_rules(world, player)
    set_location_rules(world, player)
