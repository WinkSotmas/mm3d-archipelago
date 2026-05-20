import os
from typing import Any, Dict
import yaml


DEFAULTS: Dict[str, Any] = {
    'citra_exe': 'citra-qt',
}


def load_config(path: str = 'config.yaml') -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f) or DEFAULTS
    return DEFAULTS
