import pathlib
import typing

from maison import service as config_service
from maison import types


class FakeFileSystem:
    def get_file_path(
        self, file_name: str, starting_path: typing.Optional[pathlib.Path] = None
    ) -> typing.Optional[pathlib.Path]:
        if file_name == "not.exists":
            return None
        return pathlib.Path(f"/path/to/{file_name}")


class FakeConfigReader:
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        return {
            "values": {file_path.stem: file_path.suffix},
        }


class Schema:
    def model_dump(self) -> types.ConfigValues:
        return {"key": "validated"}


class FakeValidator:
    def validate(
        self, values: types.ConfigValues, schema: type[config_service.IsSchema]
    ) -> types.ConfigValues:
        return schema().model_dump()


class TestFindConfigs:
    def test_returns_iterator_of_config_paths(self):
        service = config_service.ConfigService(
            filesystem=FakeFileSystem(),
            config_reader=FakeConfigReader(),
            validator=FakeValidator(),
        )

        configs = service.find_configs(
            source_files=["something.txt", "other.toml", "not.exists", "another.ini"]
        )

        assert list(configs) == [
            pathlib.Path("/path/to/something.txt"),
            pathlib.Path("/path/to/other.toml"),
            pathlib.Path("/path/to/another.ini"),
        ]


class TestGetConfigValues:
    @classmethod
    def setup_class(cls):
        cls.service = config_service.ConfigService(
            filesystem=FakeFileSystem(),
            config_reader=FakeConfigReader(),
            validator=FakeValidator(),
        )

    def test_returns_dict_if_config_found(self):
        config_dict = self.service.get_config_values(
            config_file_paths=[pathlib.Path("config.toml")],
            merge_configs=False,
        )

        assert config_dict == {
            "values": {"config": ".toml"},
        }

    def test_returns_first_dict_if_not_merge_configs(self):
        config_dict = self.service.get_config_values(
            config_file_paths=[pathlib.Path("config.toml"), pathlib.Path("other.ini")],
            merge_configs=False,
        )

        assert config_dict == {"values": {"config": ".toml"}}

    def test_merges_configs(self):
        config_dict = self.service.get_config_values(
            config_file_paths=[pathlib.Path("config.toml"), pathlib.Path("other.ini")],
            merge_configs=True,
        )

        assert config_dict == {
            "values": {
                "config": ".toml",
                "other": ".ini",
            }
        }


class TestValidate:
    @classmethod
    def setup_class(cls):
        cls.service = config_service.ConfigService(
            filesystem=FakeFileSystem(),
            config_reader=FakeConfigReader(),
            validator=FakeValidator(),
        )

    def test_validates_config(self):
        values = self.service.get_config_values(
            config_file_paths=[pathlib.Path("config.toml")],
            merge_configs=False,
        )

        validated_values = self.service.validate_config(values=values, schema=Schema)

        assert validated_values == {"key": "validated"}
