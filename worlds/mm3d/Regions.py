from BaseClasses import MultiWorld, Region
from .Locations import MM3DLocation, MM3D_LOCATION_TABLE, locations_by_region

# All region names used in the game.  Locations reference these by name.
MM3D_REGIONS = [
    "Menu",
    "Clock Town",
    "Southern Swamp",
    "Woodfall Temple",
    "Mountain Village",
    "Snowhead Temple",
    "Great Bay",
    "Great Bay Temple",
    "Ikana Canyon",
    "Stone Tower Temple",
    "Moon",
]

# Edges in the region graph: (source, destination).
# Rules are applied separately in Rules.py.
MM3D_CONNECTIONS = [
    ("Menu",              "Clock Town"),
    ("Clock Town",        "Southern Swamp"),
    ("Southern Swamp",    "Woodfall Temple"),
    ("Clock Town",        "Mountain Village"),
    ("Mountain Village",  "Snowhead Temple"),
    ("Clock Town",        "Great Bay"),
    ("Great Bay",         "Great Bay Temple"),
    ("Clock Town",        "Ikana Canyon"),
    ("Ikana Canyon",      "Stone Tower Temple"),
    ("Clock Town",        "Moon"),          # requires all 4 boss remains
]


def create_regions(world: MultiWorld, player: int) -> dict[str, Region]:
    """Create all MM3D regions, populate them with locations, and wire entrances."""
    loc_map = locations_by_region()
    regions: dict[str, Region] = {}

    for region_name in MM3D_REGIONS:
        region = Region(region_name, player, world)
        # Add every location that belongs to this region
        for loc_name in loc_map.get(region_name, []):
            _, offset = MM3D_LOCATION_TABLE[loc_name]
            from .Locations import get_location_id
            location = MM3DLocation(player, loc_name, get_location_id(loc_name), region)
            region.locations.append(location)
        regions[region_name] = region
        world.regions.append(region)

    # Wire entrances (rules added later in Rules.py)
    for source_name, dest_name in MM3D_CONNECTIONS:
        source = regions[source_name]
        dest   = regions[dest_name]
        source.connect(dest)

    return regions
