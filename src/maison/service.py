import pathlib
import typing
from collections.abc import Iterable


class Filesystem(typing.Protocol):
    def get_file_path(
        self, file_name: str, starting_path: typing.Optional[pathlib.Path]
    ) -> typing.Optional[pathlib.Path]: ...


class ConfigService:
    def __init__(self, filesystem: Filesystem) -> None:
        self.filesystem = filesystem

    def find_configs(
        self,
        source_files: list[str],
        starting_path: typing.Optional[pathlib.Path] = None,
    ) -> Iterable[pathlib.Path]:
        for source in source_files:
            if filepath := self.filesystem.get_file_path(
                file_name=source, starting_path=starting_path
            ):
                yield filepath

    def generate_config_dict(
        self,
        source_files: list[str],
        merge_configs: bool,
        starting_path: typing.Optional[pathlib.Path] = None,
    ) -> dict:
        pass
