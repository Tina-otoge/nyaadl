from pathlib import Path
import os
import appdirs
import yaml

from . import __title__


_default_config = {
    'command': 'webtorrent {}',
}
_config_data = None


def get(key: str) -> str:
    result = get_from_env(key)
    if result is None:
        result = get_from_config(key)
    if result is None:
        raise ValueError(f'Missing config for {key}')
    return result


def get_from_env(key: str):
    env_key = f'{__title__}_{key}'.upper()
    return os.environ.get(env_key)


def get_from_config(key: str):
    global _config_data

    config_key = key.lower()
    path = Path(appdirs.user_config_dir(__title__) + '.yml')

    if not path.exists():
        with path.open('w') as f:
            f.write('\n'.join(
                f'{key}: {value}'
                for key, value in _default_config.items()
            ))
        _config_data = _default_config

    if not _config_data:
        with path.open() as f:
            _config_data = yaml.safe_load(f)

    return _config_data.get(config_key)
