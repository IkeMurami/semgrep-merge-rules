import click
import pathlib
import typing
import urllib.request
import yaml
from yaml.scanner import ScannerError

from presets.models import Preset, PresetSource, PresetSourceURL, PresetSourceFile


def _local_preset(path: pathlib.Path) -> typing.List[Preset]:
    # Read presets from local files
    try:
        with path.open(mode='r') as inp_stream:
            presets = [
                Preset(**preset) 
                for preset in yaml.safe_load_all(inp_stream)
            ]
            
            return presets
        
    except (ScannerError, TypeError) as ex:
        raise click.BadArgumentUsage(f"YAML config is not correct: {ex}. The problem is in {path.name}")
    except Exception as ex:
        raise click.BadArgumentUsage(f"YAML Local file reader: something wrong: {ex}. The problem is in {path.name}")


def _remote_preset(url: str) -> typing.List[Preset]:
    # Download presets from remote repositories
    try:
        with urllib.request.urlopen(url) as inp_stream:
            presets = [
                # print(preset)
                Preset(**preset) 
                for preset in yaml.safe_load_all(inp_stream)
            ]

            return presets

    except (ScannerError, TypeError) as ex:
        raise click.BadArgumentUsage(f"YAML config is not correct: {ex}. The problem is in {url}")
    except Exception as ex:
        raise click.BadArgumentUsage(f"YAML Downloader: something wrong: {ex}. The problem is in {url}")


def load_presets(ctx, param: click.Argument, value: typing.Tuple[PresetSource]) -> typing.List[Preset]:
    # Check schemas of preset files and download them
    presets = list()
    for preset_file_path in value:
        preset = preset_file_path.preset
        
        if isinstance(preset, PresetSourceFile):
            # print('Is file', preset.file_path)
            presets.extend(
                _local_preset(pathlib.Path(preset.file_path))
            )
            
        elif isinstance(preset, PresetSourceURL):
            # print('Is URL', preset.url)
            presets.extend(
                _remote_preset(preset.url)
            )
    
    return presets