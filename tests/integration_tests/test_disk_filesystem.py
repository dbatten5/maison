import pathlib

from maison import disk_filesystem


class TestGetFilePath:
    def test_get_file_path_finds_in_current_dir(self, tmp_path: pathlib.Path):
        fs = disk_filesystem.DiskFilesystem()

        file = tmp_path / "settings.json"
        _ = file.write_text("{}")

        result = fs.get_file_path("settings.json", starting_path=tmp_path)

        assert result == file

    def test_get_file_path_traverses_up(self, tmp_path: pathlib.Path):
        fs = disk_filesystem.DiskFilesystem()

        nested = tmp_path / "a" / "b"
        nested.mkdir(parents=True)

        file = tmp_path / "a" / "target.txt"
        _ = file.write_text("found me")

        result = fs.get_file_path("target.txt", starting_path=nested)

        assert result == file

    def test_get_file_path_with_absolute_path(self, tmp_path: pathlib.Path):
        fs = disk_filesystem.DiskFilesystem()

        file = tmp_path / "absolute.txt"
        _ = file.write_text("hello")

        result = fs.get_file_path(str(file))

        assert result == file

    def test_get_file_path_returns_none_if_not_found(self):
        fs = disk_filesystem.DiskFilesystem()

        result = fs.get_file_path("ghost.ini")

        assert result is None


class TestOpenFile:
    def test_opens_file(self, tmp_path: pathlib.Path):
        fs = disk_filesystem.DiskFilesystem()

        file = tmp_path / "thing.txt"
        _ = file.write_text("hello")

        result = fs.open_file(path=file)

        assert result.read() == b"hello"
