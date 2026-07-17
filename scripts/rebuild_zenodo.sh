#!/usr/bin/env bash
# Full rebuild: arxiv.md → zenodo.tex, figures, zenodo.pdf, dist/zenodo_submit.zip
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Generating zenodo.tex and figures"
python3 scripts/build_arxiv_tex.py --target zenodo

echo "==> Compiling zenodo.pdf"
latexmk -pdf -interaction=nonstopmode -jobname=zenodo zenodo.tex

echo "==> Packaging Zenodo submit zip"
./scripts/package_zenodo.sh --zip-only
