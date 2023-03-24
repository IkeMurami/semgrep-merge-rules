import click
import pathlib
import pydantic
import typing
from urllib.parse import urlparse


class PresetSourceURL(pydantic.BaseModel):
    url: str

class PresetSourceFile(pydantic.BaseModel):
    file_path: str

class PresetSource(pydantic.BaseModel):
    preset: PresetSourceURL | PresetSourceFile

class ClickPresetOutput(click.ParamType):
    name = "OUTPUT"

    def convert(self, 
                value: typing.Any, 
                param: typing.Optional[click.Parameter], 
                ctx: typing.Optional[click.Context]) -> pathlib.Path:
        output = click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True)
        output_path = output.convert(value, param, ctx)

        return pathlib.Path(output_path)

class ClickPresetSource(click.ParamType):
    name = "URL"

    def convert(self, 
                value: typing.Any, 
                param: typing.Optional[click.Parameter], 
                ctx: typing.Optional[click.Context]) -> PresetSource:
        
        # Try parse as a file
        
        try:
            click_path = click.Path(exists=True, readable=True, resolve_path=True)
            file_path = click_path.convert(value, param, ctx)

            return PresetSource(**{
                'preset': PresetSourceFile(**{
                    'file_path': file_path
                })
            })
        except Exception:
            ...

        # Try parse as a URL
        try:
            url = urlparse(value)
            
            return PresetSource(**{
                'preset': PresetSourceURL(**{
                    'url': value
                })
            })
        except Exception as ex:
            ...
        
        self.fail(f'{value!r} is not a valid preset source', param, ctx)


OUTPUT = ClickPresetOutput()
PRESET_SOURCE = ClickPresetSource()
