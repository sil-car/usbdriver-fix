#!/usr/bin/env bash
# shellcheck disable=SC1091

# Create venv.
env=buildenv  # has to match folder name in app.spec
if python3 --version >/dev/null; then
    python3 -m venv "$env"
else
    python -m venv "$env"
fi
# Enter venv.
if [[ -d $env/bin ]]; then
    source "$env/bin/activate"
else
    source "$env/scripts/activate"
fi
# Build package.
python -m pip install pyinstaller
python -m pip install .
# Build executable.
pyinstaller --clean app.spec
# Exit venv.
deactivate
# Remove venv.
rm -rf "$env"
