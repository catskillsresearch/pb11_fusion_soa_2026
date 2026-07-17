# Zenodo deposit

## Metadata: `.zenodo.json` is authoritative

For categorization and deposit metadata, **edit `.zenodo.json` only**.

| File | Role |
|------|------|
| **`.zenodo.json`** | **Primary.** Resource type, LOC `subjects`, keywords, creators, license, GitHub link, version. Used by Zenodo upload autofill and GitHub–Zenodo release sync. |
| `CITATION.cff` | **Secondary.** Minimal file so GitHub can show “Cite this repository.” Zenodo **ignores** it when `.zenodo.json` is present. |

When both files exist in the repo root, [Zenodo’s GitHub integration uses only `.zenodo.json`](https://help.zenodo.org/docs/github/describe-software/zenodo-json/).

## GitHub vs Zenodo

**GitHub** — canonical source (`arxiv.md`, figures, build scripts). Repository licensed **Apache-2.0**.

**Zenodo** — citable **DOI** for `zenodo.pdf`. Publication licensed **CC-BY-4.0**. No full-repo upload required.

This survey is **not** submitted to arXiv physics (author not endorsed there). The PDF title page carries no arXiv subject classes.

## Build outputs

| File | Purpose |
|------|---------|
| `zenodo.tex` / `zenodo.pdf` | Deposit PDF (technical report; no arXiv categories) |
| `.zenodo.json` | **Edit this for categorization** |
| `arxiv.tex` / `arxiv.pdf` | Optional local build (also without arXiv categories) |

```bash
./scripts/rebuild_zenodo.sh      # zenodo.pdf + dist/zenodo_submit.zip
bash scripts/build_arxiv_pdf.sh  # optional arXiv-shaped local PDF
```

## Current `.zenodo.json` categorization

| Field | Value |
|-------|--------|
| Resource type | Publication → **Report** |
| Access | Open |
| Language | English |
| License | **CC-BY-4.0** (publication); GitHub repo remains Apache-2.0 |
| Keywords | proton-boron fusion, p-11B, aneutronic fusion, … |
| Subjects (LOC) | Nuclear fusion · Fusion reactors · Plasma · Nuclear engineering · Boron |
| Related ID | GitHub repo (`isSupplementedBy`) |
| Version | 1.0.0 |

PDF title page mirrors this: **Resource type: Technical report** (no arXiv subject classes).

## Upload

1. `./scripts/package_zenodo.sh` (or `./scripts/rebuild_zenodo.sh` for a full rebuild)
2. [zenodo.org/deposit/new](https://zenodo.org/deposit/new)
3. Upload `dist/zenodo_submit.zip` (`zenodo.pdf` + `.zenodo.json`)
4. Confirm metadata, publish, add DOI to `preferred-citation` in `CITATION.cff` if you want GitHub to show it

## Citation (after upload)

```text
Ericson, L. W. (2026). State of the art on proton-boron fusion for electricity
generation (Version 1.0.0) [Report]. Zenodo.
https://doi.org/10.5281/zenodo.XXXXXXX
```

Source: https://github.com/catskillsresearch/pb11_fusion_soa_2026
