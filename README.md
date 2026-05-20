# mm3d-archipelago
This is an attempt to create an AP World for MM3D, starting out with citra only and then passing to 3ds hardware.

## Overview

This repository will provide an Archipelago-compatible randomizer integration for "Majora's Mask 3D" (MM3D). The initial focus is Citra-only workflows; later support for real 3DS hardware will be added.

## External references

- MM3D Randomizer (reference): https://github.com/Z3DR/MM3D_Randomizer
- ALBW Archipelago (reference): https://github.com/randomsalience/albw-archipelago

These projects are used as design references and external dependencies; this repo does not embed their code.

## Quickstart (Citra-only)

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Provide a patched ROM from the MM3D randomizer or a vanilla MM3D ROM to be patched with an external tool.

3. Launch a randomized session with Citra:

```bash
python -m mm3d_archipelago.cli start /path/to/mm3d.3ds
```

## Next steps

- Integrate Archipelago multiworld client to sync items and goals.
- Automate patching using `MM3D_Randomizer` CLI when available.
- Add support for flashing to 3DS hardware.
