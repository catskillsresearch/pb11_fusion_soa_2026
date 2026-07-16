#!/usr/bin/env python3
r"""Convert arxiv.md to arxiv.tex (arXiv-ready).

Adapted from catskillsresearch/scott_models (and scott1982) without Lean/code-appendix
machinery. Pipeline:

  1. Read ``arxiv.md``; lift ``## Abstract`` into ``\\begin{abstract}``.
  2. Convert ``research/figures/*`` assets to pdfLaTeX-safe copies under ``figures/assets/``.
  3. Render `` ```mermaid `` fences to ``figures/figure-NNN.pdf`` via mermaid-cli.
  4. Strip manual section numbers; pandoc → LaTeX; splice figure/code placeholders.
  5. Emit a single ``arxiv.tex`` for one-shot latexmk / arXiv pdfLaTeX.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent

SRC = ROOT / "arxiv.md"
OUT = ROOT / "arxiv.tex"
PREAMBLE = SCRIPTS / "tex_preamble_arxiv.tex"
LISTINGS_DIR = ROOT / "listings"
FIGURES_DIR = ROOT / "figures"
ASSETS_DIR = FIGURES_DIR / "assets"
RESEARCH_FIGURES = ROOT / "research" / "figures"
PUPPETEER_CONFIG = SCRIPTS / "puppeteer-config.json"
_WRITTEN_LISTINGS: set[Path] = set()
_WRITTEN_ASSETS: set[Path] = set()

AUTHOR = "Lars Warren Ericson"
COMPANY = "Catskills Research Company"
GITHUB_URL = r"https://github.com/catskillsresearch/pb11_fusion_soa_2026"
ORCID = "0000-0001-8299-9361"
EMAIL = "lars.ericson@catskillsresearch.com"

GITHUB_INLINE_MATH = re.compile(r"\$`([^`\n]+?)`\$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FENCE_RE = re.compile(r"^```([^\n]*)\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
MANUAL_SECTION_NUM = re.compile(r"^(#{1,6})[ \t]+\d+(?:\.\d+)*\.?[ \t]+", re.MULTILINE)
# Alt text may contain citation brackets like [89]; match via the path marker.
MD_IMAGE_MARKER = "](research/figures/"

PROSE_ASCII_FALLBACKS: tuple[tuple[str, str], ...] = (
    ("\u26a0\ufe0f", "Warning:"),
    ("\u26a0", "Warning:"),
    ("\u2705", r"\ensuremath{\checkmark}"),
    ("\u2611", r"\ensuremath{\checkmark}"),
    ("\u2610", "[ ]"),
)


def find_chrome() -> str | None:
    env = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def extract_title() -> str:
    first = SRC.read_text(encoding="utf-8").splitlines()[0]
    title = first[2:].strip() if first.startswith("# ") else first.strip()
    title = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", title)
    return title


TITLE = extract_title()


def apply_prose_ascii_fallbacks(text: str) -> str:
    for src, dst in PROSE_ASCII_FALLBACKS:
        text = text.replace(src, dst)
    text = re.sub(r"(.)\u20d7", r"\1-vec", text)
    return text


def github_math_to_tex(text: str) -> str:
    return GITHUB_INLINE_MATH.sub(r"$\1$", text)


def strip_html_comments(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        body = match.group(0)
        if re.match(r"<!--\s*mermaid-(caption|landscape)\b", body, re.IGNORECASE):
            return body
        return ""

    return HTML_COMMENT.sub(repl, text)


def strip_manual_section_numbers(text: str) -> str:
    return MANUAL_SECTION_NUM.sub(r"\1 ", text)


def strip_title_line(text: str) -> str:
    """Drop only the leading ``# Title`` line (keep Abstract; ``---`` is a horizontal rule)."""
    if text.startswith("# "):
        return text[text.find("\n") + 1 :].lstrip("\n")
    return text


def extract_abstract(text: str) -> tuple[str, str]:
    m = re.search(r"^##\s+Abstract\s*\n(.*?)(?=^##\s)", text, re.DOTALL | re.MULTILINE)
    if not m:
        return "", text
    abstract_md = m.group(1).strip()
    # Drop a trailing markdown thematic break left after the abstract.
    abstract_md = re.sub(r"\n---\s*$", "", abstract_md).strip()
    body = text[: m.start()] + text[m.end() :]
    body = re.sub(r"^\n*---\n+", "\n", body)
    return abstract_md, body


def render_mermaid(code: str, idx: int, *, scale: float = 1.0) -> str:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    mmd_path = FIGURES_DIR / f"figure-{idx:03d}.mmd"
    meta_path = FIGURES_DIR / f"figure-{idx:03d}.meta"
    pdf_path = FIGURES_DIR / f"figure-{idx:03d}.pdf"
    code_stripped = code.strip() + "\n"
    cache_key = f"scale={scale}\n{code_stripped}"
    if (
        mmd_path.is_file()
        and meta_path.is_file()
        and pdf_path.is_file()
        and meta_path.read_text(encoding="utf-8") == cache_key
    ):
        return pdf_path.relative_to(ROOT).as_posix()
    mmd_path.write_text(code_stripped, encoding="utf-8")
    meta_path.write_text(cache_key, encoding="utf-8")

    mmdc = shutil.which("mmdc")
    if not mmdc:
        raise RuntimeError(
            "mermaid-cli (mmdc) not found; install with "
            "`npm install -g @mermaid-js/mermaid-cli`"
        )
    env = os.environ.copy()
    chrome = find_chrome()
    if chrome:
        env["PUPPETEER_EXECUTABLE_PATH"] = chrome
    cmd = [
        mmdc,
        "-i",
        str(mmd_path),
        "-o",
        str(pdf_path),
        "--pdfFit",
        "-b",
        "transparent",
        "-s",
        str(scale),
    ]
    if PUPPETEER_CONFIG.is_file():
        cmd += ["-p", str(PUPPETEER_CONFIG)]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not pdf_path.is_file():
        sys.stderr.write(proc.stdout + "\n" + proc.stderr + "\n")
        raise RuntimeError(f"mmdc failed to render figure {idx}")
    return pdf_path.relative_to(ROOT).as_posix()


def convert_research_asset(src_name: str) -> str:
    """Copy/convert ``research/figures/<src_name>`` → ``figures/assets/<safe>``."""
    src = RESEARCH_FIGURES / src_name
    if not src.is_file():
        raise FileNotFoundError(f"missing figure asset: {src}")

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(src_name).stem
    suffix = Path(src_name).suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg", ".pdf"}:
        dest = ASSETS_DIR / src.name
        if not dest.is_file() or dest.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dest)
        _WRITTEN_ASSETS.add(dest.resolve())
        return dest.relative_to(ROOT).as_posix()

    if suffix == ".webp":
        dest = ASSETS_DIR / f"{stem}.png"
        if not dest.is_file() or dest.stat().st_mtime < src.stat().st_mtime:
            from PIL import Image

            Image.open(src).convert("RGB").save(dest, format="PNG", optimize=True)
        _WRITTEN_ASSETS.add(dest.resolve())
        return dest.relative_to(ROOT).as_posix()

    if suffix == ".svg":
        dest = ASSETS_DIR / f"{stem}.pdf"
        if not dest.is_file() or dest.stat().st_mtime < src.stat().st_mtime:
            convert = shutil.which("convert")
            if not convert:
                raise RuntimeError("ImageMagick `convert` required for SVG→PDF")
            proc = subprocess.run(
                [convert, str(src), str(dest)],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode != 0 or not dest.is_file():
                sys.stderr.write(proc.stdout + "\n" + proc.stderr + "\n")
                raise RuntimeError(f"SVG conversion failed for {src_name}")
        _WRITTEN_ASSETS.add(dest.resolve())
        return dest.relative_to(ROOT).as_posix()

    raise RuntimeError(f"unsupported figure type: {src_name}")


def caption_md_to_latex(caption: str) -> str:
    """Convert a one-line markdown figure caption to LaTeX (math, cite brackets, emph)."""
    caption = caption.strip()
    if not caption:
        return ""
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--wrap=none"],
        input=caption,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pandoc caption failed: {proc.stderr}")
    out = proc.stdout.strip()
    out = re.sub(r"\s+\n\s*", " ", out)
    out = out.replace("\n", " ")
    return out


def replace_markdown_images(text: str) -> tuple[str, dict[str, str]]:
    """Turn ``![caption](research/figures/…)`` into captioned figure placeholders.

    Captions may contain ``]`` (e.g. ``[89]``), so parsing keys off the path marker
    rather than a naive ``[^\\]]*`` alt match.
    """
    placeholders: dict[str, str] = {}
    parts: list[str] = []
    pos = 0
    idx = 0
    while True:
        marker_at = text.find(MD_IMAGE_MARKER, pos)
        if marker_at < 0:
            parts.append(text[pos:])
            break
        start = text.rfind("![", pos, marker_at)
        if start < 0:
            parts.append(text[pos : marker_at + 2])
            pos = marker_at + 2
            continue
        path_start = marker_at + len("](")
        path_end = text.find(")", path_start)
        if path_end < 0:
            parts.append(text[pos : marker_at + 2])
            pos = marker_at + 2
            continue
        alt = text[start + 2 : marker_at]
        src_path = text[path_start:path_end]
        if not src_path.startswith("research/figures/"):
            parts.append(text[pos : marker_at + 2])
            pos = marker_at + 2
            continue
        src_name = src_path[len("research/figures/") :]
        rel = convert_research_asset(src_name)
        caption_tex = caption_md_to_latex(github_math_to_tex(alt))
        slug = re.sub(r"[^a-z0-9]+", "-", alt.lower()).strip("-")[:48] or str(idx + 1)
        key = f"ASSETINCLUDE{idx:03d}"
        placeholders[key] = figure_latex(rel, caption_tex, f"fig:asset-{slug}")
        parts.append(text[pos:start])
        parts.append(f"\n\n{key}\n\n")
        pos = path_end + 1
        idx += 1
    return "".join(parts), placeholders


def prune_stale_assets() -> None:
    if not ASSETS_DIR.is_dir():
        return
    for path in ASSETS_DIR.iterdir():
        if path.is_file() and path.resolve() not in _WRITTEN_ASSETS:
            path.unlink()


def extract_mermaid_meta(text: str) -> list[tuple[str, bool]]:
    """Return ``(caption, landscape)`` for each mermaid fence in document order."""
    meta: list[tuple[str, bool]] = []
    caption_comment = re.compile(
        r"<!--\s*mermaid-caption:\s*(.+?)\s*-->", re.IGNORECASE
    )
    landscape_comment = re.compile(r"<!--\s*mermaid-landscape\s*-->", re.IGNORECASE)
    for m in re.finditer(r"^```mermaid\s*$", text, re.MULTILINE):
        prefix_lines = text[: m.start()].splitlines()[-8:]
        explicit = None
        landscape = False
        for line in reversed(prefix_lines):
            stripped = line.strip()
            if not stripped:
                continue
            if landscape_comment.fullmatch(stripped):
                landscape = True
                continue
            cm = caption_comment.fullmatch(stripped)
            if cm:
                explicit = cm.group(1).strip().rstrip(".")
                break
            # Stop scanning once we hit non-meta prose.
            if not stripped.startswith("<!--"):
                break
        if explicit:
            caption = f"{explicit}."
        else:
            heading = None
            for line in reversed(text[: m.start()].splitlines()):
                hm = re.match(r"^#{2,4}\s+(.+)$", line.strip())
                if hm:
                    heading = hm.group(1).strip()
                    break
            if heading:
                heading = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", heading)
                caption = f"{heading}."
            else:
                caption = f"Diagram {len(meta) + 1}."
        meta.append((caption, landscape))
    return meta


def figure_latex(
    rel_path: str, caption: str, label: str, *, landscape: bool = False
) -> str:
    # Landscape: long page edge becomes \\linewidth, so wide LR charts can grow.
    include = (
        f"\\includegraphics[width=\\linewidth,"
        f"height=0.82\\textheight,keepaspectratio]{{{rel_path}}}"
        if landscape
        else (
            f"\\includegraphics[max width=\\linewidth,"
            f"max totalheight=0.85\\textheight,keepaspectratio]{{{rel_path}}}"
        )
    )
    body = (
        "\\begin{figure}[p]\n"
        "\\centering\n"
        f"{include}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}\n"
        if landscape
        else (
            "\\begin{figure}[htbp]\n"
            "\\centering\n"
            f"{include}\n"
            f"\\caption{{{caption}}}\n"
            f"\\label{{{label}}}\n"
            "\\end{figure}\n"
        )
    )
    if landscape:
        return "\\begin{landscape}\n" + body + "\\end{landscape}\n"
    return body


def write_listing(code: str, listing_name: str) -> str:
    LISTINGS_DIR.mkdir(parents=True, exist_ok=True)
    # Keep listings ASCII-ish for pdfLaTeX safety.
    source = code.rstrip("\n").encode("ascii", errors="replace").decode("ascii")
    listing_path = LISTINGS_DIR / listing_name
    write_if_changed(listing_path, source + "\n")
    _WRITTEN_LISTINGS.add(listing_path.resolve())
    return listing_path.relative_to(ROOT).as_posix()


def prune_stale_listings() -> None:
    if not LISTINGS_DIR.is_dir():
        return
    for path in LISTINGS_DIR.iterdir():
        if path.is_file() and path.resolve() not in _WRITTEN_LISTINGS:
            path.unlink()


def replace_fences(text: str) -> tuple[str, dict[str, str]]:
    mermaid_meta = extract_mermaid_meta(text)
    placeholders: dict[str, str] = {}
    other_idx = 0
    mermaid_idx = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal other_idx, mermaid_idx
        lang = match.group(1).strip().lower()
        body = match.group(2)
        if lang == "math":
            key = f"MATHINCLUDE{other_idx:03d}"
            other_idx += 1
            placeholders[key] = f"\\[\n{body.strip()}\n\\]\n"
            return f"\n\n{key}\n\n"
        if lang == "mermaid":
            key = f"FIGINCLUDE{other_idx:03d}"
            caption, landscape = (
                mermaid_meta[mermaid_idx]
                if mermaid_idx < len(mermaid_meta)
                else (f"Diagram {mermaid_idx + 1}.", False)
            )
            # Landscape charts get a higher raster/vector scale for sharper labels.
            scale = 2.0 if landscape else 1.25
            rel_path = render_mermaid(body, mermaid_idx, scale=scale)
            # Escape special TeX chars lightly in captions from headings.
            caption_tex = (
                caption.replace("\\", "\\textbackslash{}")
                .replace("&", "\\&")
                .replace("%", "\\%")
                .replace("#", "\\#")
                .replace("_", "\\_")
            )
            slug = re.sub(r"[^a-z0-9]+", "-", caption.lower()).strip("-")[:48] or str(
                mermaid_idx + 1
            )
            label = f"fig:mermaid-{slug}"
            mermaid_idx += 1
            other_idx += 1
            placeholders[key] = figure_latex(
                rel_path, caption_tex, label, landscape=landscape
            )
            return f"\n\n{key}\n\n"
        key = f"CODEINCLUDE{other_idx:03d}"
        rel_path = write_listing(body, f"snippet-{other_idx:03d}.txt")
        other_idx += 1
        placeholders[key] = f"\\lstinputlisting[style=codebox]{{{rel_path}}}\n"
        return f"\n\n{key}\n\n"

    converted = FENCE_RE.sub(repl, text)
    return converted, placeholders


def pandoc_to_latex(markdown: str, shift: bool = True) -> str:
    cmd = [
        "pandoc",
        "-f",
        "markdown+tex_math_dollars+raw_tex+smart",
        "-t",
        "latex",
        "--wrap=none",
    ]
    if shift:
        cmd += ["--shift-heading-level-by=-1"]
    proc = subprocess.run(cmd, input=markdown, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError("pandoc failed")
    return proc.stdout


def inject_placeholders(latex: str, placeholders: dict[str, str]) -> str:
    out = latex
    for key, value in placeholders.items():
        patterns = [
            key,
            f"\\emph{{{key}}}",
            f"\\text{{{key}}}",
            f"\\passthrough{{\\lstinline!{key}!}}",
        ]
        for pat in patterns:
            if pat in out:
                out = out.replace(pat, value)
                break
        else:
            out = out.replace(key, value)
    return out


def _gate_symbols(cell: str) -> str:
    """Map scoreboard glyphs to compact one-em macros."""
    cell = cell.strip()
    repl = {
        "●": r"\gateF{}",
        "◐": r"\gateP{}",
        "○": r"\gateW{}",
        "---": r"\gateNA{}",
        "—": r"\gateNA{}",
        "–": r"\gateNA{}",
    }
    return repl.get(cell, cell)


def _strip_heading_block_before(latex: str, lt_start: int, title_substr: str) -> int:
    """Return start index to cut from, dropping hypertarget + subsection for a Table heading."""
    # Look back for \subsection{Table ...} or \hypertarget{table-...}
    window = latex[max(0, lt_start - 800) : lt_start]
    # Prefer hypertarget that mentions table
    ht = window.rfind(r"\hypertarget{table-")
    if ht >= 0:
        return max(0, lt_start - 800) + ht
    sub = window.rfind(r"\subsection{")
    if sub >= 0 and title_substr.lower() in window[sub:].lower():
        return max(0, lt_start - 800) + sub
    return lt_start


def rebuild_table_a_matrix(latex: str) -> str:
    """Table A as a single-page captioned float (not a page-breaking longtable)."""
    marker = r"Table A: Four-axis"
    start = latex.find(marker)
    if start < 0:
        return latex
    lt_start = latex.find(r"\begin{longtable}", start)
    if lt_start < 0:
        return latex
    lt_end = latex.find(r"\end{longtable}", lt_start)
    if lt_end < 0:
        return latex
    lt_end += len(r"\end{longtable}")
    wrap_start = _strip_heading_block_before(latex, lt_start, "Table A")

    # Pull data rows from the pandoc longtable body.
    block = latex[lt_start:lt_end]
    rows: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.count("&") != 2 or not s.endswith(r"\\"):
            continue
        if "Axis" in s and "Question" in s:
            continue
        if s.startswith(r"\textbf{") or s.startswith("Time") or "Confinement" in s or "Fuel" in s or "Kinetics" in s:
            rows.append(s if s.endswith(r"\\") else s + r" \\")
    # Keep only the four axis rows (prefer \textbf{…} forms).
    bold_rows = [r for r in rows if r.startswith(r"\textbf{")]
    if len(bold_rows) >= 4:
        rows = bold_rows[:4]
    elif len(rows) < 4:
        return latex

    # Keep caption + body together (non-float); page break is inserted before §1.2.
    new_table = (
        "\\begin{center}\n"
        "\\small\n"
        "\\surveycaptionof{Table A}{Four-axis mental matrix (how to read any pitch)}\n"
        "\\label{tab:matrix-axes}\n"
        "\\begin{tabularx}{\\linewidth}{@{}>{\\bfseries}l>{\\raggedright\\arraybackslash}X"
        ">{\\raggedright\\arraybackslash}X@{}}\n"
        "\\toprule\n"
        "Axis & Question in plain language & Typical answers in this survey \\\\\n"
        "\\midrule\n"
        + "\n".join(rows)
        + "\n"
        "\\bottomrule\n"
        "\\end{tabularx}\n"
        "\\end{center}\n"
    )
    return latex[:wrap_start] + new_table + latex[lt_end:]


def rebuild_table4_rankings(latex: str) -> str:
    """Table 4 as captioned landscape longtable; timelines in one column (no crushed dates)."""
    marker = r"Table 4: Ranked"
    start = latex.find(marker)
    if start < 0:
        return latex
    lt_start = latex.find(r"\begin{longtable}", start)
    if lt_start < 0:
        return latex
    lt_end = latex.find(r"\end{longtable}", lt_start)
    if lt_end < 0:
        return latex
    lt_end += len(r"\end{longtable}")
    block = latex[lt_start:lt_end]
    wrap_start = _strip_heading_block_before(latex, lt_start, "Table 4")

    rows: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.count("&") != 8 or not s.endswith(r"\\"):
            continue
        if "Rank" in s and "Path" in s:
            continue
        cells = [c.strip() for c in s[:-2].split(" & ")]
        if len(cells) != 9:
            continue
        rank_plain = re.sub(r"[^\d]", "", cells[0])
        if not rank_plain:
            continue
        # Rank Path Type POS kappa POS* Q Proto Grid → merge last three
        timelines = (
            f"$Q\\gtrsim 1$: {cells[6]}\\newline "
            f"Proto: {cells[7]}\\newline "
            f"Grid: {cells[8]}"
        )
        rows.append(
            " & ".join([cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], timelines])
            + r" \\"
        )

    if len(rows) < 5:
        return latex

    new_table = (
        "\\begin{landscape}\n"
        "\\footnotesize\n"
        "\\setlength{\\tabcolsep}{5pt}\n"
        "\\renewcommand{\\arraystretch}{1.2}\n"
        "\\begin{longtable}{@{}\n"
        "  c\n"
        "  >{\\raggedright\\arraybackslash}p{4.2cm}\n"
        "  >{\\raggedright\\arraybackslash}p{2.8cm}\n"
        "  c c c\n"
        "  >{\\raggedright\\arraybackslash}p{5.8cm}@{}}\n"
        "\\surveycaption{Table 4}{Ranked $p\\text{-}^{11}\\text{B}$ plant odds "
        "(editorial, mid-2026)}\\label{tab:plant-odds}\\\\\n"
        "\\toprule\n"
        "\\textbf{Rank} & \\textbf{Path} & \\textbf{Type} & "
        "\\textbf{POS} & $\\boldsymbol{\\kappa}$ & \\textbf{POS$\\star$} & "
        "\\textbf{Timelines} \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\surveycaptioncont{Table 4: Ranked plant odds (continued)}\\\\\n"
        "\\toprule\n"
        "\\textbf{Rank} & \\textbf{Path} & \\textbf{Type} & "
        "\\textbf{POS} & $\\boldsymbol{\\kappa}$ & \\textbf{POS$\\star$} & "
        "\\textbf{Timelines} \\\\\n"
        "\\midrule\n"
        "\\endhead\n"
        "\\bottomrule\n"
        "\\endlastfoot\n"
        + "\n".join(rows)
        + "\n\\end{longtable}\n"
        "\\end{landscape}\n"
    )
    return latex[:wrap_start] + new_table + latex[lt_end:]


def rebuild_table2a_footprint(latex: str) -> str:
    """Table 2a as captioned longtable with readable column widths."""
    marker = r"Table 2a: Corporate"
    start = latex.find(marker)
    if start < 0:
        start = latex.find("Corporate / brand legal footprint")
    if start < 0:
        return latex
    lt_start = latex.find(r"\begin{longtable}", start)
    if lt_start < 0:
        return latex
    lt_end = latex.find(r"\end{longtable}", lt_start)
    if lt_end < 0:
        return latex
    lt_end += len(r"\end{longtable}")
    block = latex[lt_start:lt_end]
    wrap_start = _strip_heading_block_before(latex, lt_start, "Table 2a")

    rows: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.count("&") != 4 or not s.endswith(r"\\"):
            continue
        if "Entity" in s and "Domain" in s:
            continue
        cells = [c.strip() for c in s[:-2].split(" & ")]
        if len(cells) != 5:
            continue
        if not cells[0].startswith(r"\textbf{"):
            continue
        rows.append(" & ".join(cells) + r" \\")

    if len(rows) < 3:
        return latex

    new_table = (
        "\\footnotesize\n"
        "\\setlength{\\tabcolsep}{4pt}\n"
        "\\begin{longtable}{@{}\n"
        "  >{\\raggedright\\arraybackslash}p{2.6cm}\n"
        "  >{\\raggedright\\arraybackslash}p{2.4cm}\n"
        "  >{\\raggedright\\arraybackslash}p{3.4cm}\n"
        "  >{\\raggedright\\arraybackslash}p{2.6cm}\n"
        "  >{\\raggedright\\arraybackslash}p{4.2cm}@{}}\n"
        "\\surveycaption{Table 2a}{Corporate / brand legal footprint (non-patent)}"
        "\\label{tab:legal-footprint}\\\\\n"
        "\\toprule\n"
        "\\textbf{Entity} & \\textbf{Domain} & \\textbf{Corp.\\ entity} & "
        "\\textbf{USPTO TM} & \\textbf{Notes} \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\surveycaptioncont{Table 2a: Corporate / brand legal footprint (continued)}\\\\\n"
        "\\toprule\n"
        "\\textbf{Entity} & \\textbf{Domain} & \\textbf{Corp.\\ entity} & "
        "\\textbf{USPTO TM} & \\textbf{Notes} \\\\\n"
        "\\midrule\n"
        "\\endhead\n"
        "\\bottomrule\n"
        "\\endlastfoot\n"
        + "\n".join(rows)
        + "\n\\end{longtable}\n"
    )
    return latex[:wrap_start] + new_table + latex[lt_end:]


def rebuild_table1_scorecard(latex: str) -> str:
    """Table 1 as captioned landscape scorecard (no subsection numbering)."""
    marker = r"Table 1: Zeroth-order scorecard"
    start = latex.find(marker)
    if start < 0:
        return latex
    lt_start = latex.find(r"\begin{longtable}", start)
    if lt_start < 0:
        # may already be rebuilt; try after landscape
        return latex
    lt_end = latex.find(r"\end{longtable}", lt_start)
    if lt_end < 0:
        return latex
    lt_end += len(r"\end{longtable}")
    block = latex[lt_start:lt_end]
    wrap_start = _strip_heading_block_before(latex, lt_start, "Table 1")

    rows: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith(r"\textbf{") and " & " in s and s.endswith(r"\\"):
            cells = [c.strip() for c in s[:-2].split(" & ")]
            if len(cells) < 12:
                continue
            project, conf = cells[0], cells[1]
            gates = [_gate_symbols(c) for c in cells[2:11]]
            notes = cells[11]
            row = " & ".join([project, conf, *gates, notes]) + r" \\"
            rows.append(row)

    if not rows:
        return latex

    new_table = (
        "\\begin{landscape}\n"
        "\\footnotesize\n"
        "\\setlength{\\tabcolsep}{3pt}\n"
        "\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{longtable}{@{}\n"
        "  >{\\raggedright\\arraybackslash}p{2.55cm}\n"
        "  >{\\raggedright\\arraybackslash}p{1.55cm}\n"
        "  *{9}{c}\n"
        "  >{\\raggedright\\arraybackslash}p{8.8cm}@{}}\n"
        "\\surveycaption{Table 1}{Zeroth-order scorecard for key projects "
        "(State of the Art, 2026)}\\label{tab:scorecard}\\\\\n"
        "\\toprule\n"
        "\\textbf{Project} & \\textbf{C} & "
        "\\textbf{F} & \\textbf{K} & \\textbf{R} & \\textbf{A} & "
        "\\textbf{L} & \\textbf{M} & \\textbf{T} & \\textbf{S} & \\textbf{H} & "
        "\\textbf{Notes (2025--2026)} \\\\\n"
        "\\midrule\n"
        "\\endfirsthead\n"
        "\\surveycaptioncont{Table 1: Zeroth-order scorecard (continued)}\\\\\n"
        "\\toprule\n"
        "\\textbf{Project} & \\textbf{C} & "
        "\\textbf{F} & \\textbf{K} & \\textbf{R} & \\textbf{A} & "
        "\\textbf{L} & \\textbf{M} & \\textbf{T} & \\textbf{S} & \\textbf{H} & "
        "\\textbf{Notes (2025--2026)} \\\\\n"
        "\\midrule\n"
        "\\endhead\n"
        "\\bottomrule\n"
        "\\endlastfoot\n"
        + "\n".join(rows)
        + "\n\\end{longtable}\n"
        "\\end{landscape}\n"
    )
    return latex[:wrap_start] + new_table + latex[lt_end:]


def promote_remaining_survey_tables(latex: str) -> str:
    """Turn leftover ``\\subsection{Table …}`` + longtable into captioned longtables.

    Pandoc puts the header in ``\\endhead`` only, so a caption there would re-enter
    the List of Tables on every page. Split into ``\\endfirsthead`` / ``\\endhead``.
    """
    pattern = re.compile(
        r"(?:\\hypertarget\{[^}]*\}\{%\s*)?"
        r"\\(?:sub)*section\{(Table\s+[^:}]+):\s*([^}]+)\}\\label\{[^}]*\}\s*"
        r"(?:\}\s*)?",
        re.DOTALL,
    )

    def slugify(tab_id: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", tab_id.lower()).strip("-")

    matches = list(pattern.finditer(latex))
    for m in reversed(matches):
        tab_id = m.group(1).strip()
        title = m.group(2).strip()
        if tab_id in {"Table 1", "Table 2a", "Table 4", "Table A"}:
            latex = latex[: m.start()] + latex[m.end() :]
            continue
        lt_start = latex.find(r"\begin{longtable}", m.end())
        if lt_start < 0 or lt_start - m.end() > 400:
            latex = latex[: m.start()] + latex[m.end() :]
            continue
        top = latex.find(r"\toprule", lt_start)
        if top < 0:
            continue
        endhead = latex.find(r"\endhead", top)
        if endhead < 0 or endhead - top > 4000:
            continue
        header_block = latex[top:endhead]
        label = f"tab:{slugify(tab_id)}"
        first = (
            f"\\surveycaption{{{tab_id}}}{{{title}}}\\label{{{label}}}\\\\\n"
            f"{header_block}"
            f"\\endfirsthead\n"
            f"\\surveycaptioncont{{{tab_id}: {title} (continued)}}\\\\\n"
            f"{header_block}"
            f"\\endhead"
        )
        latex = (
            latex[: m.start()]
            + latex[m.end() : top]
            + first
            + latex[endhead + len(r"\endhead") :]
        )
    return latex


def cleanup_pandoc_latex(latex: str) -> str:
    latex = latex.replace("\\pandocbounded{", "{")
    latex = re.sub(r"\\tightlist\n", "", latex)
    for cmd in ("section", "subsection", "subsubsection", "paragraph"):
        latex = re.sub(
            rf"(\\{cmd}\{{)\d+(?:\.\d+)*\.?\s+",
            r"\1",
            latex,
        )
    # Pandoc emits bare \includegraphics{path} for markdown images; scale to page.
    latex = re.sub(
        r"\\includegraphics\{([^}]+)\}",
        r"\\includegraphics[max width=\\linewidth,"
        r"max totalheight=0.72\\textheight,keepaspectratio]{\1}",
        latex,
    )
    # Score glyphs anywhere (legend prose + other tables)
    latex = (
        latex.replace("●", r"\gateF{}")
        .replace("◐", r"\gateP{}")
        .replace("○", r"\gateW{}")
    )
    latex = rebuild_table_a_matrix(latex)
    # Start §1.2 on a fresh page so Table A caption is not orphaned at a page bottom.
    latex = re.sub(
        r"(\\hypertarget\{a-tidy-mental-matrix-four-axes\}\{%\s*)"
        r"(\\subsection\{A tidy mental matrix)",
        r"\\clearpage\n\1\2",
        latex,
        count=1,
    )
    latex = rebuild_table1_scorecard(latex)
    latex = rebuild_table2a_footprint(latex)
    latex = rebuild_table4_rankings(latex)
    latex = promote_remaining_survey_tables(latex)
    latex = re.sub(r"\n{3,}", "\n\n", latex)
    return latex


def insert_lists_of_floats(latex: str) -> str:
    """Insert List of Tables + List of Figures after the abstract block."""
    lists = (
        "\\clearpage\n"
        "\\listoftables\n\n"
        "\\listoffigures\n"
        "\\clearpage\n\n"
    )
    # Prefer right after abstract
    abs_end = latex.find(r"\end{abstract}")
    if abs_end >= 0:
        insert_at = abs_end + len(r"\end{abstract}")
        # skip following whitespace
        return latex[:insert_at] + "\n\n" + lists + latex[insert_at:].lstrip("\n")
    marker = r"\hypertarget{references}{%"
    if marker in latex:
        return latex.replace(marker, lists + marker, 1)
    return latex


def cleanup_abstract_latex(latex: str) -> str:
    latex = latex.replace("\\pandocbounded{", "{")
    latex = latex.replace("\\textbf{{[}", "\\textbf{[")
    latex = latex.replace("\\texttt{{[}", "\\texttt{[")
    latex = latex.replace("{]}}", "]}")
    latex = re.sub(r"\\begin\{center\}\\rule\{.*?\}\\end\{center\}\s*", "", latex, flags=re.DOTALL)
    return latex


def build_title_page(abstract_latex: str) -> str:
    return textwrap.dedent(
        f"""
        \\title{{\\textbf{{{TITLE}}}}}

        \\author[1]{{\\textbf{{{AUTHOR}}}}}
        \\affil[1]{{{COMPANY}}}
        \\affil[1]{{\\url{{{GITHUB_URL}}}}}
        \\affil[1]{{\\texttt{{{EMAIL}}}}}

        \\date{{\\today}}

        \\begin{{document}}

        \\maketitle

        \\begin{{center}}
          \\small
          \\textbf{{ORCID:}} {ORCID} \\\\
          \\textbf{{Primary Category:}} physics.plasm-ph (Plasma Physics) \\\\
          \\textbf{{Secondary Category:}} physics.app-ph (Applied Physics)
        \\end{{center}}

        \\begin{{abstract}}
        {abstract_latex.strip()}
        \\end{{abstract}}
        """
    ).strip()


def build_document(preamble: str, title_page: str, body: str) -> str:
    head = "\\ifdefined\\pdfoutput\\pdfoutput=1\\fi\n\n"
    return head + preamble + "\n\n" + title_page + "\n\n" + body + "\n\n\\end{document}\n"


def main() -> int:
    if not SRC.is_file():
        print(f"error: missing {SRC}", file=sys.stderr)
        return 1
    if not PREAMBLE.is_file():
        print(f"error: missing {PREAMBLE}", file=sys.stderr)
        return 1

    for d in (LISTINGS_DIR, FIGURES_DIR, ASSETS_DIR):
        d.mkdir(parents=True, exist_ok=True)
    _WRITTEN_LISTINGS.clear()
    _WRITTEN_ASSETS.clear()

    raw = SRC.read_text(encoding="utf-8")
    body = strip_title_line(raw)
    body = apply_prose_ascii_fallbacks(body)
    body = strip_html_comments(body)
    abstract_md, body = extract_abstract(body)
    body = strip_manual_section_numbers(body)
    body, image_placeholders = replace_markdown_images(body)
    body = github_math_to_tex(body)
    body, placeholders = replace_fences(body)
    placeholders = {**image_placeholders, **placeholders}
    prune_stale_listings()
    prune_stale_assets()

    latex_body = pandoc_to_latex(body, shift=True)
    latex_body = inject_placeholders(latex_body, placeholders)
    latex_body = cleanup_pandoc_latex(latex_body)

    abstract_latex = (
        pandoc_to_latex(github_math_to_tex(abstract_md), shift=False) if abstract_md else ""
    )
    abstract_latex = cleanup_abstract_latex(abstract_latex)

    preamble = PREAMBLE.read_text(encoding="utf-8")
    title_page = build_title_page(abstract_latex)
    # LoT/LoF belong after the abstract on the title page, not in the pandoc body.
    document = build_document(preamble, insert_lists_of_floats(title_page), latex_body)
    changed = write_if_changed(OUT, document)
    n_listings = (
        sum(1 for p in LISTINGS_DIR.iterdir() if p.is_file()) if LISTINGS_DIR.is_dir() else 0
    )
    n_mermaid = sum(1 for p in FIGURES_DIR.glob("figure-*.pdf"))
    n_assets = sum(1 for p in ASSETS_DIR.iterdir() if p.is_file()) if ASSETS_DIR.is_dir() else 0
    note = "updated" if changed else "unchanged"
    print(
        f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes, "
        f"from arxiv.md, {n_listings} snippet listings, "
        f"{n_mermaid} mermaid figures, {n_assets} raster/SVG assets, {note})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
