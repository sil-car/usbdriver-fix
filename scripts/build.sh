#!/usr/bin/env bash

# Create venv.
env=buildenv  # has to match folder name in app.spec
python3 -m venv "$env"
# Enter venv.
source "./$env/bin/activate"
# Build package.
python3 -m pip install .
# Build executable.
pyinstaller --clean app.spec
# Exit venv.
deactivate
# Remove venv.
rm -rf "$env"
