Majora's Mask 3D — Archipelago Integration Design

Goal
----
Provide an Archipelago-compatible randomizer workflow for Majora's Mask 3D (MM3D), starting with Citra-only operation. This document outlines integration options, recommended MVP, and implementation steps.

References
----------
- MM3D Randomizer (reference): https://github.com/Z3DR/MM3D_Randomizer
- ALBW Archipelago (reference): https://github.com/randomsalience/albw-archipelago

High-level architecture
-----------------------
- CLI (`mm3d_archipelago.cli`): user-facing commands to start a session, connect to Archipelago, and build or patch ROMs.
- Patching layer: responsible for producing a Citra-loadable ROM. Two modes:
  - Prepatch mode (MVP): call an external `MM3D_Randomizer` CLI (user-provided) to create a per-slot patched ROM before running Citra.
  - Runtime mode (advanced): connect to the Archipelago server and apply item grants at runtime via memory injection or by using a custom patcher that supports multiworld item streams.
- Archipelago client: use the official `archipelago-client` (Python) to handle multiworld connections, authentication, item/flag exchange, and slot settings.
- Citra launcher: starts Citra with the selected ROM and optional debugging hooks.

Recommended MVP
-----------------
1. Require the user to run `MM3D_Randomizer` externally to generate a patched ROM per-player/slot. The CLI will accept that ROM and launch Citra.
2. Implement Archipelago client skeleton to authenticate and fetch slot information (no in-game injection yet). Use this to coordinate seeds and to publish player status to the multiworld.
3. Provide an explicit workflow for creating Archipelago multiworld sessions with the existing MM3D randomizer tooling (documented in README).

Integration options (detailed)
------------------------------
- Option A — External patcher (MVP):
  - Pros: simple, robust, no runtime hacking.
  - Cons: requires `MM3D_Randomizer` CLI and per-slot ROM generation; cannot dynamically receive items.
- Option B — Runtime injection (Phase 2):
  - Pros: full multiworld behavior (receive items live).
  - Cons: complex: requires writing to Citra process memory or building a ROM mod that polls an external bridge.
- Option C — Hybrid: use Archipelago for seed coordination and have the randomizer produce a ROM that includes placeholders which can be filled via a runtime bridge.

Data flow examples
------------------
- Prepatch flow (MVP):
  1. Player runs `mm3d-archipelago build --seed <seed> --slot <slot>` which delegates to `MM3D_Randomizer` to produce `mm3d_<slot>.3ds`.
  2. Player runs `mm3d-archipelago start mm3d_<slot>.3ds` which launches Citra.

- Runtime flow (Phase 2):
  1. `mm3d-archipelago connect` authenticates to archipelago and opens item stream.
  2. On item receive, the client writes to Citra process memory or triggers an in-ROM handler that grants items.

Security & legality
-------------------
- This repository must not include copyrighted ROMs or any distributed MM3D assets.
- Users are required to provide their own legally obtained ROMs and any external randomizer tools.

Next implementation steps
-------------------------
1. Implement CLI commands to accept a ROM and launch Citra (done).
2. Add `mm3d_archipelago.archipelago_client` implementation using `archipelago-client` (next).
3. Document how to generate per-slot ROMs using `MM3D_Randomizer` and recommended CLI flags.
4. Prototype live-item injection using Citra memory writes or an in-ROM bridge (later).

Notes
-----
Where possible the project will follow the patterns used by the referenced `albw-archipelago` project for multiworld handling and `MM3D_Randomizer` for patching. The repository will only reference those projects and will not copy their code.
