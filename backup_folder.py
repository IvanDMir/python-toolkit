import tarfile
import argparse
from pathlib import Path
from datetime import datetime
import sys

def exclude(tarinfo):
    if ".venv" in tarinfo.name.split("/"):
        return None
    return tarinfo


parser = argparse.ArgumentParser(description="backups desired folder")

parser.add_argument("carpeta")

args = parser.parse_args()

ruta = Path(args.carpeta).resolve()

if not ruta.exists():
        print(f"the chosen route does not exist",file=sys.stderr)
        sys.exit(1)
if not ruta.is_dir():
        print(f"The chosen route is not a folder",file=sys.stderr)
        sys.exit(2)
today = datetime.now()
date_format = today.strftime("%Y-%m-%d-%H%M")

backup_Name = f"{ruta.name}_{date_format}.tar.gz"

with tarfile.open(backup_Name,"w:gz") as tar:
	tar.add(ruta, arcname=ruta.name,filter=exclude)

print(f"Backup for {backup_Name} Created")
