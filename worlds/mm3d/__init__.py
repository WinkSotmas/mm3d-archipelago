"""Majora's Mask 3D — Archipelago World definition.

Targets the 3DS remake (MM3D).  Initial support is Citra-only; 3DS hardware
support is planned for a later phase.

See DESIGN.md in the repository root for the full architecture plan.
"""

from BaseClasses import MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .Items import (
    MM3DItem,
    MM3D_ITEM_TABLE,
    FILLER_ITEMS,
    create_item,
    get_item_id,
)
from .Locations import MM3DLocation, MM3D_LOCATION_TABLE, get_location_id
from .Regions import create_regions
from .Rules import set_rules
from .Options import MM3DOptions


class MM3DWebWorld(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Majora's Mask 3D for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["WinkSotmas"],
        )
    ]


class MM3DWorld(World):
    """Majora's Mask 3D — the 2015 Nintendo 3DS remake of the N64 classic.

    Stop the moon from falling on Clock Town by collecting all four boss remains
    and defeating Majora.  Items, masks, songs, and dungeon keys are shuffled
    across the multiworld.
    """

    game = "Majora's Mask 3D"
    options_dataclass = MM3DOptions
    options: MM3DOptions

    web = MM3DWebWorld()

    # Item and location name → ID mappings required by AP
    item_name_to_id: dict[str, int] = {
        name: get_item_id(name)
        for name, (_, offset) in MM3D_ITEM_TABLE.items()
        if offset is not None
    }
    location_name_to_id: dict[str, int] = {
        name: get_location_id(name)
        for name in MM3D_LOCATION_TABLE
    }

    # ── World generation lifecycle ──────────────────────────────────────────

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)
        self._place_victory_event()

    def _place_victory_event(self) -> None:
        """Place a locked Victory event at the Moon location."""
        moon_loc = self.multiworld.get_location("Moon - Defeat Majora", self.player)
        victory  = MM3DItem("Victory", ItemClassification.progression, None, self.player)
        moon_loc.place_locked_item(victory)

    def create_items(self) -> None:
        """Populate the item pool based on player options."""
        exclude = {"Victory"}  # events never go in the pool

        # Determine which item categories to include
        items_to_place = []
        for name in MM3D_ITEM_TABLE:
            if name in exclude:
                continue
            _, offset = MM3D_ITEM_TABLE[name]
            if offset is None:
                continue  # skip other events

            # Respect options: skip dungeon items / masks / songs if turned off
            if not self.options.shuffle_masks and self._is_mask(name):
                continue
            if not self.options.shuffle_songs and self._is_song(name):
                continue

            items_to_place.append(name)

        # Create and register each item
        for name in items_to_place:
            self.multiworld.itempool.append(create_item(name, self.player))

        # Pad with filler to match location count
        loc_count  = len(self.location_name_to_id)
        item_count = len(items_to_place)
        filler_needed = max(0, loc_count - item_count - 1)  # -1 for Victory event

        import random
        for _ in range(filler_needed):
            filler_name = random.choice(FILLER_ITEMS)
            self.multiworld.itempool.append(create_item(filler_name, self.player))

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)
        # Win condition: have the Victory item (placed at Moon - Defeat Majora)
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has("Victory", self.player)
        )

    # ── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _is_mask(name: str) -> bool:
        mask_keywords = (
            "Mask", "Hat", "Hood", "Helmet",
        )
        return any(k in name for k in mask_keywords)

    @staticmethod
    def _is_song(name: str) -> bool:
        song_keywords = (
            "Song", "Sonata", "Lullaby", "Bossa", "Elegy", "Oath", "Scarecrow",
            "Epona",
        )
        return any(k in name for k in song_keywords)

    # ── Output generation ────────────────────────────────────────────────────

    def generate_output(self, output_directory: str) -> None:
        """Generate a spoiler-compatible data file for the Citra client.

        The client reads this to know which item lives at which location so
        it can apply memory patches when the player checks a location.

        TODO: replace with a proper patch format once the Citra memory map
        is documented.
        """
        import json
        import os
        from BaseClasses import LocationProgressType

        data: dict[str, str] = {}
        for location in self.multiworld.get_filled_locations(self.player):
            if location.item and location.address is not None:
                data[location.name] = location.item.name

        filename = os.path.join(
            output_directory,
            f"MM3D_{self.multiworld.seed_name}_P{self.player}"
            f"_{self.multiworld.get_file_safe_player_name(self.player)}.json",
        )
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
