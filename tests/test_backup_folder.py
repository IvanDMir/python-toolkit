import tarfile

import pytest

from backup_folder import create_backup, validate_source


def test_validate_source_fails_if_path_does_not_exist(tmp_path):
    missing_path = tmp_path / "does_not_exist"

    with pytest.raises(FileNotFoundError):
        validate_source(missing_path)


def test_create_backup_excludes_venv_and_pycache(tmp_path):
    source = tmp_path / "project"
    source.mkdir()
    (source / "file.txt").write_text("content")
    (source / ".venv").mkdir()
    (source / ".venv" / "file.txt").write_text("virtual environment")
    (source / "__pycache__").mkdir()
    (source / "__pycache__" / "module.pyc").write_bytes(b"cache")

    backup_path, _ = create_backup(
        source,
        tmp_path / "backups",
        tmp_path / "backup.log",
    )

    with tarfile.open(backup_path, "r:gz") as archive:
        names = archive.getnames()

    assert "project/file.txt" in names
    assert not any(".venv" in name for name in names)
    assert not any("__pycache__" in name for name in names)


def test_create_backup_does_not_include_previous_backups(tmp_path):
    source = tmp_path / "project"
    source.mkdir()
    (source / "file.txt").write_text("content")
    backup_dir = source / "backups"

    first_backup, _ = create_backup(
        source,
        backup_dir,
        tmp_path / "backup.log",
    )
    second_backup, _ = create_backup(
        source,
        backup_dir,
        tmp_path / "backup.log",
    )

    assert first_backup != second_backup
    with tarfile.open(second_backup, "r:gz") as archive:
        names = archive.getnames()

    assert "project/file.txt" in names
    assert not any("backups" in name for name in names)