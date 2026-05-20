from Options import (
    Toggle,
    Choice,
    Range,
    PerGameCommonOptions,
)
from dataclasses import dataclass


class ShuffleDungeonItems(Choice):
    """Controls whether dungeon-specific items (maps, compasses, small keys, boss keys) are shuffled.

    - own_dungeon: keys stay in their own dungeon (vanilla-like)
    - any_dungeon: keys can appear in any dungeon
    - anywhere: keys can appear anywhere in the multiworld
    """
    display_name = "Shuffle Dungeon Items"
    option_own_dungeon  = 0
    option_any_dungeon  = 1
    option_anywhere     = 2
    default = 0


class ShuffleMasks(Toggle):
    """If enabled, all 24 masks (excluding transformation masks) are shuffled into the item pool."""
    display_name = "Shuffle Masks"
    default = 1


class ShuffleSongs(Toggle):
    """If enabled, learned songs are shuffled into the item pool."""
    display_name = "Shuffle Songs"
    default = 1


class StartingTime(Choice):
    """Which in-game time the player starts at on Day 1.

    Does not affect cycle logic but can open or close time-sensitive checks.
    """
    display_name = "Starting Time"
    option_dawn    = 0   # ~6:00 AM
    option_morning = 1   # ~8:00 AM
    option_noon    = 2   # ~12:00 PM (default)
    option_evening = 3   # ~6:00 PM
    default = 2


class LogicDifficulty(Choice):
    """Controls how strict the logic is.

    - normal: standard logic, no glitches assumed
    - hard:   minor tricks allowed (e.g. tight item-timing windows)
    - glitched: advanced out-of-bounds and movement glitches in logic
    """
    display_name = "Logic Difficulty"
    option_normal   = 0
    option_hard     = 1
    option_glitched = 2
    default = 0


class FillerItemCount(Range):
    """Number of extra filler items (rupees, magic jars) added to pad the pool."""
    display_name = "Filler Item Count"
    range_start = 0
    range_end   = 20
    default     = 5


@dataclass
class MM3DOptions(PerGameCommonOptions):
    shuffle_dungeon_items: ShuffleDungeonItems
    shuffle_masks:         ShuffleMasks
    shuffle_songs:         ShuffleSongs
    starting_time:         StartingTime
    logic_difficulty:      LogicDifficulty
    filler_item_count:     FillerItemCount
