import tarfile
import argparse
import logging
from pathlib import Path
from datetime import datetime
import sys

# Guarda los mensajes en backup.log y también los muestra en la terminal.
log_path = Path("backup.log").resolve()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="backups desired folder")

parser.add_argument("carpeta")

args = parser.parse_args()

logger.info("Backup started for: %s", args.carpeta)

ruta = Path(args.carpeta).resolve()

if not ruta.exists():
    logger.error("The chosen path does not exist: %s", ruta)
    sys.exit(1)
if not ruta.is_dir():
    logger.error("The chosen path is not a folder: %s", ruta)
    sys.exit(1)

today = datetime.now()
date_format = today.strftime("%Y-%m-%d_%H-%M-%S")

backup_dir = Path("backups").resolve()
backup_name = f"{ruta.name}_{date_format}.tar.gz"
backup_path = backup_dir / backup_name


# ver qué rutas se deberian excluir;
try:
    backup_relative_path = backup_dir.relative_to(ruta)
except ValueError:
    backup_relative_path = None

try:
    log_relative_path = log_path.relative_to(ruta)
except ValueError:
    log_relative_path = None

# Evita incluir el entorno virtual
def exclude(tarinfo):
    archive_parts = Path(tarinfo.name).parts
    if ".venv" in archive_parts:
        return None

    relative_parts = archive_parts[1:] if archive_parts and archive_parts[0] == ruta.name else archive_parts
    if backup_relative_path is not None:
        backup_parts = backup_relative_path.parts
        if relative_parts[:len(backup_parts)] == backup_parts:
            return None
    if log_relative_path is not None and relative_parts == log_relative_path.parts:
        return None

    return tarinfo

# Crea un nombre nuevo para el respaldo
backup_created = False

try:
    backup_dir.mkdir(parents=True, exist_ok=True)
    with backup_path.open("xb"):
        backup_created = True
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(ruta, arcname=ruta.name, filter=exclude)
    backup_size = backup_path.stat().st_size
except (OSError, tarfile.TarError) as error:
    if backup_created:
        try:
            backup_path.unlink(missing_ok=True)
        except OSError as cleanup_error:
            logger.error("Could not remove incomplete backup %s: %s", backup_path, cleanup_error)
    logger.error("Backup failed: %s", error)
    sys.exit(1)
logger.info("Backup generated: %s (size: %d bytes)", backup_path, backup_size)
