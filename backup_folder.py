import argparse
import logging
import sys
import tarfile
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Create a backup of a folder")
    parser.add_argument("carpeta", help="Folder to back up")
    return parser.parse_args()


def setup_logging():
    log_path = Path("backup.log").resolve()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(),
        ],
    )
    return log_path


def validate_source(source):
    source_path = Path(source).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"The chosen path does not exist: {source_path}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"The chosen path is not a folder: {source_path}")
    return source_path


def create_backup(source, backup_dir, log_path):
    date_format = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    backup_name = f"{source.name}_{date_format}.tar.gz"
    backup_path = backup_dir / backup_name

    try:
        backup_relative_path = backup_dir.relative_to(source)
    except ValueError:
        backup_relative_path = None

    try:
        log_relative_path = log_path.relative_to(source)
    except ValueError:
        log_relative_path = None

    def exclude(tarinfo):
        archive_parts = Path(tarinfo.name).parts
        #if ".venv" in archive_parts or "__pycache__" in archive_parts:
         #   return None

        relative_parts = archive_parts
        if archive_parts and archive_parts[0] == source.name:
            relative_parts = archive_parts[1:]

        if backup_relative_path is not None:
            backup_parts = backup_relative_path.parts
            if relative_parts[:len(backup_parts)] == backup_parts:
                return None
        if log_relative_path is not None and relative_parts == log_relative_path.parts:
            return None

        return tarinfo

    backup_created = False
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        with backup_path.open("xb"):
            backup_created = True
        with tarfile.open(backup_path, "w:gz") as archive:
            archive.add(source, arcname=source.name, filter=exclude)
    except (OSError, tarfile.TarError):
        if backup_created:
            try:
                backup_path.unlink(missing_ok=True)
            except OSError as cleanup_error:
                logger.error("Could not remove incomplete backup %s: %s", backup_path, cleanup_error)
        raise

    return backup_path, backup_path.stat().st_size


def main():
    try:
        args = parse_args()
        log_path = setup_logging()
        logger.info("Backup started for: %s", args.carpeta)
        source = validate_source(args.carpeta)
        backup_dir = Path("backups").resolve()
        backup_path, backup_size = create_backup(source, backup_dir, log_path)
        logger.info("Backup generated: %s (size: %d bytes)", backup_path, backup_size)
    except (OSError, tarfile.TarError) as error:
        logger.error("Backup failed: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
