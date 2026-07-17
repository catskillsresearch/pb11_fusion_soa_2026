# pb11_fusion_soa_2026

An AI-generated survey article on the **state of the art in proton-boron (p–¹¹B) fusion in 2026**.

Intended for distribution via [Zenodo](https://zenodo.org/) (citable DOI). The author is not endorsed for arXiv physics, so this deposit does **not** use arXiv subject classes; see [ZENODO.md](ZENODO.md).

*Note on authorship: This article was generated using Large Language Model (LLM) AI tools. It is a synthesis of publicly available literature and may contain AI-generated artifacts, citation errors, or factual hallucinations. It must be rigorously verified by the reader before any scientific, engineering, or policy use.*

## Layout

- `arxiv.md` — source narrative (edit this)
- `research/` — archived PDFs and figure credits
- `scripts/` — TeX/PDF/Zenodo packaging (Zenodo path ported from `fusion_reactor_component_failures`)
- `.zenodo.json` — authoritative Zenodo deposit metadata
- `CITATION.cff` — GitHub “Cite this repository” only

## Build (Zenodo)

```bash
./scripts/rebuild_zenodo.sh       # zenodo.pdf + dist/zenodo_submit.zip
# or step-wise:
./scripts/build_zenodo_tex.sh     # arxiv.md → zenodo.tex + figures/
./scripts/package_zenodo.sh       # zip zenodo.pdf + .zenodo.json
```

Upload `dist/zenodo_submit.zip` at [zenodo.org/deposit/new](https://zenodo.org/deposit/new). Details: [ZENODO.md](ZENODO.md).

## Build (optional local arXiv-shaped PDF)

Same manuscript, no arXiv categories on the title page:

```bash
bash scripts/build_arxiv_pdf.sh   # arxiv.pdf + dist/arxiv_submit.zip
```

Requires: `pandoc`, `mmdc` (mermaid-cli), ImageMagick `convert`, `latexmk` + LuaLaTeX (local), Chrome/Chromium for mermaid.

## License

Apache License 2.0 (see `LICENSE` and `NOTICE`). Zenodo publication metadata requests **CC-BY-4.0** for the deposited PDF (see `.zenodo.json`).

## Contributions and Collaboration

This repository functions strictly as a unilateral broadcast of public work for educational and research purposes.

* **Pull Requests and Issues:** This project does not accept external Pull Requests, contributions, or modifications, and tracking features have been disabled. Any external collaboration vectors are closed.
* **Forks:** Users are entirely free and encouraged to fork or clone this repository to modify the materials on their own profiles in accordance with the repository's Apache 2.0 License.

## Regulatory and Liability Disclaimer

* **Limitations:** The survey provided herein is for theoretical research and academic purposes only. It does not constitute engineering specifications, operational guidance, or advice for physical fusion systems.
* **Liability Protection:** In accordance with Section 8 of the Apache 2.0 License, this work is provided "AS IS" without warranties of any kind. Catskills Research Company disclaims all liability for any direct, indirect, consequential damages resulting from the use, misuse, or reliance on this survey.
