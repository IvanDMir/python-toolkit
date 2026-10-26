# python-toolkit

![Tests](https://github.com/IvanDMir/python-toolkit/actions/workflows/tests.yml/badge.svg)

Python scripts for automating system administration tasks.

## Tools

### backup_folder.py
Creates a compressed `.tar.gz` backup of a folder.

- Timestamped backup names, so runs never overwrite each other
- Excludes `.venv`, `__pycache__`, and its own backups and log
- Logs to `backup.log` and the console
- Removes incomplete backups if something fails

## Installation

```bash
git clone git@github.com:IvanDMir/python-toolkit.git
cd python-toolkit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Usage

```bash
python backup_folder.py <folder>
```

Example:

```bash
python backup_folder.py ~/projects/my-project
```

Backups are saved in `backups/`.

## Tests

```bash
pytest -v
```

Tests run automatically on every push with GitHub Actions.

## Project structure

```
python-toolkit/
├── .github/workflows/tests.yml   # CI pipeline
├── backup_folder.py              # Backup script
├── tests/                        # pytest tests
└── requirements-dev.txt          # Dependencies
```