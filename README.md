# pb11_fusion_soa_2026

An AI-generated survey article on the **state of the art in proton-boron (p–¹¹B) fusion in 2026**.

Intended for distribution via [arXiv](https://arxiv.org/); if that is not available, via [Zenodo](https://zenodo.org/).

*Note on authorship: This article was generated using Large Language Model (LLM) AI tools. It is a synthesis of publicly available literature and may contain AI-generated artifacts, citation errors, or factual hallucinations. It must be rigorously verified by the reader before any scientific, engineering, or policy use.*

## Layout

- `arxiv.md` — source narrative (edit this)
- `research/` — archived PDFs and figure credits
- `scripts/` — arXiv TeX/PDF/dist pipeline (ported from `scott_models` / `scott1982`, without Lean)

## Build (arXiv)

```bash
bash scripts/build_arxiv_tex.sh      # arxiv.md → arxiv.tex + figures/
bash scripts/build_arxiv_pdf.sh      # compile PDF + package dist/arxiv_submit.zip
# or, if tex already built:
bash scripts/package_arxiv_submit.sh --skip-tex-build
```

Requires: `pandoc`, `mmdc` (mermaid-cli), ImageMagick `convert`, `latexmk` + LuaLaTeX (local), Chrome/Chromium for mermaid.

Generated artifacts (`arxiv.tex`, `figures/`, `dist/`, …) are gitignored; upload `dist/arxiv_submit.zip` to arXiv (pdfLaTeX).

## License

Apache License 2.0 (see `LICENSE` and `NOTICE`).

## Contributions and Collaboration

This repository functions strictly as a unilateral broadcast of public work for educational and research purposes.

* **Pull Requests and Issues:** This project does not accept external Pull Requests, contributions, or modifications, and tracking features have been disabled. Any external collaboration vectors are closed.
* **Forks:** Users are entirely free and encouraged to fork or clone this repository to modify the materials on their own profiles in accordance with the repository's Apache 2.0 License.

## Regulatory and Liability Disclaimer

* **Limitations:** The survey provided herein is for theoretical research and academic purposes only. It does not constitute engineering specifications, operational guidance, or advice for physical fusion systems.
* **Liability Protection:** In accordance with Section 8 of the Apache 2.0 License, this work is provided "AS IS" without warranties of any kind. Catskills Research Company disclaims all liability for any direct, indirect, consequential damages resulting from the use, misuse, or reliance on this survey.
