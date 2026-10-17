import argparse
from pathlib import Path
import sys
parser = argparse.ArgumentParser(description="backups desired folder")

parser.add_argument("carpeta")

args = parser.parse_args()

ruta = Path(args.carpeta)

if not ruta.exists():
        print(f"the chosen route does not exist",file=sys.stderr)
        sys.exit(1)
else:
        if not ruta.is_dir():
           print(f"The chosen route is not a folder",file=sys.stderr)
           sys.exit(2)
		
print(f"Backup folder {ruta}")   
