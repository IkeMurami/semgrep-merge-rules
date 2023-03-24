import asyncio
import itertools
import pathlib
import typing
import yaml

from presets.models import Preset


async def merge_presets(presets: typing.List[Preset], output: pathlib.Path):
    
    tasks = map(
        lambda item: asyncio.create_task(
            item.process()
        ),
        itertools.chain.from_iterable(
            itertools.filterfalse(
                lambda item: item is None,
                map(
                    lambda item: item.preset, 
                    presets
                )
            )
        )
    )

    processed_rules = await asyncio.gather(*tasks)
    processed_rules = itertools.chain.from_iterable(processed_rules)
    
    big_semgrep_rule = dict(
        rules=list(processed_rules)
    )

    with output.open(mode='w') as out_stream:
        yaml.dump(big_semgrep_rule, out_stream)

