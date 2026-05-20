import subprocess
from typing import Sequence, Optional


def launch_citra(citra_exe: str, rom_path: str, extra_args: Optional[Sequence[str]] = None) -> subprocess.Popen:
    """Launch Citra with the specified ROM. Returns the Popen handle.

    This is a minimal Citra launcher used for Citra-only workflows.
    """
    args = [citra_exe, rom_path]
    if extra_args:
        args.extend(list(extra_args))
    return subprocess.Popen(args)
