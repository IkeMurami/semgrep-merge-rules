import asyncio
import click
import pathlib
import typing

from presets import load_presets, merge_presets
from presets.models import OUTPUT, PRESET_SOURCE, Preset
from presets import merge



@click.command()
@click.option(
    '-o', '--output', 'output', 
    required=False, 
    default='preset.yaml', 
    type=OUTPUT, 
    help="The one big Semgrep rule"
)
@click.argument(
    'presets', 
    nargs=-1, 
    required=True, 
    type=PRESET_SOURCE, 
    callback=load_presets, 
    # help="Rule presets (YAML)"
)
def main(presets: typing.List[Preset], output: str):

    asyncio.run(
        merge_presets(
            presets, 
            pathlib.Path(output)
        )
    )