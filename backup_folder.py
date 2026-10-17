import argparse

parser = argparse.ArgumentParser()

parser.add_argument("Ruta")
args = parser.parse_args()

print(f"Voy a respaldar: {args.Ruta}")
