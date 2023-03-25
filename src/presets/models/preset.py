import itertools
import pathlib
import pydantic
import typing
from urllib.parse import urlparse
import urllib.request
import yaml


class Rule(pydantic.BaseModel):
    url: typing.Optional[str]
    path: typing.Optional[str]
    ids: typing.Optional[typing.List[str]]

    @staticmethod
    async def _extract_semgrep_rules(rule_ids: typing.List[str], inp_stream) -> typing.List:
        yaml_obj = yaml.safe_load_all(inp_stream)
        
        rules = itertools.filterfalse(
            lambda item: rule_ids and item['id'] not in rule_ids,
            itertools.chain.from_iterable(
                map(
                    lambda item: item['rules'], 
                    yaml_obj
                )
            )
        )

        return list(rules)

    async def _load(self, callback) -> None:
        if self.url:
            with urllib.request.urlopen(self.url) as inp_stream:
                return await callback(self.ids, inp_stream)
        
        if self.path:
            with pathlib.Path(self.path).open(mode='r') as inp_stream:
                return await callback(self.ids, inp_stream)
        
        return list()

    async def process(self) -> typing.List:

        return await self._load(Rule._extract_semgrep_rules)
        

class Preset(pydantic.BaseModel):
    preset: typing.Optional[typing.List[Rule]]