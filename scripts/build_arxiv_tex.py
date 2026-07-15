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
MD_IMAGE_RE = re.compile(
    r"!\[([^\]]*)\]\((research/figures/([^)\s]+))\)"
)

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
        if re.match(r"<!--\s*mermaid-caption:", body, re.IGNORECASE):
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


def render_mermaid(code: str, idx: int) -> str:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    mmd_path = FIGURES_DIR / f"figure-{idx:03d}.mmd"
    pdf_path = FIGURES_DIR / f"figure-{idx:03d}.pdf"
    code_stripped = code.strip() + "\n"
    if (
        mmd_path.is_file()
        and pdf_path.is_file()
        and mmd_path.read_text(encoding="utf-8") == code_stripped
    ):
        return pdf_path.relative_to(ROOT).as_posix()
    mmd_path.write_text(code_stripped, encoding="utf-8")

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
    cmd = [mmdc, "-i", str(mmd_path), "-o", str(pdf_path), "--pdfFit", "-b", "transparent"]
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


def rewrite_markdown_images(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        alt = match.group(1)
        src_name = match.group(3)
        rel = convert_research_asset(src_name)
        return f"![{alt}]({rel})"

    return MD_IMAGE_RE.sub(repl, text)


def prune_stale_assets() -> None:
    if not ASSETS_DIR.is_dir():
        return
    for path in ASSETS_DIR.iterdir():
        if path.is_file() and path.resolve() not in _WRITTEN_ASSETS:
            path.unlink()


def extract_mermaid_captions(text: str) -> list[str]:
    captions: list[str] = []
    caption_comment = re.compile(
        r"<!--\s*mermaid-caption:\s*(.+?)\s*-->", re.IGNORECASE
    )
    for m in re.finditer(r"^```mermaid\s*$", text, re.MULTILINE):
        prefix = text[: m.start()]
        explicit = None
        for line in reversed(prefix.splitlines()[-6:]):
            stripped = line.strip()
            if not stripped:
                continue
            cm = caption_comment.fullmatch(stripped)
            if cm:
                explicit = cm.group(1).strip().rstrip(".")
            break
        if explicit:
            captions.append(f"{explicit}.")
            continue
        heading = None
        for line in reversed(prefix.splitlines()):
            hm = re.match(r"^#{2,4}\s+(.+)$", line.strip())
            if hm:
                heading = hm.group(1).strip()
                break
        if heading:
            heading = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", heading)
            captions.append(f"{heading}.")
        else:
            captions.append(f"Diagram {len(captions) + 1}.")
    return captions


def figure_latex(rel_path: str, caption: str, label: str) -> str:
    return (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[max width=\\linewidth,"
        f"max totalheight=0.85\\textheight,keepaspectratio]{{{rel_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}\n"
    )


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
    mermaid_captions = extract_mermaid_captions(text)
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
            rel_path = render_mermaid(body, mermaid_idx)
            caption = (
                mermaid_captions[mermaid_idx]
                if mermaid_idx < len(mermaid_captions)
                else f"Diagram {mermaid_idx + 1}."
            )
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
            placeholders[key] = figure_latex(rel_path, caption_tex, label)
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
    latex = re.sub(r"\n{3,}", "\n\n", latex)
    return latex


def insert_list_of_figures(latex: str) -> str:
    marker = r"\hypertarget{references}{%"
    if marker not in latex:
        # Fallback: before \section{References}
        alt = r"\section{References}"
        if alt in latex:
            return latex.replace(alt, r"\listoffigures" + "\n\n" + alt, 1)
        return latex
    return latex.replace(marker, r"\listoffigures" + "\n\n" + marker, 1)


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
    body = rewrite_markdown_images(body)
    body = github_math_to_tex(body)
    body, placeholders = replace_fences(body)
    prune_stale_listings()
    prune_stale_assets()

    latex_body = pandoc_to_latex(body, shift=True)
    latex_body = inject_placeholders(latex_body, placeholders)
    latex_body = cleanup_pandoc_latex(latex_body)
    latex_body = insert_list_of_figures(latex_body)

    abstract_latex = (
        pandoc_to_latex(github_math_to_tex(abstract_md), shift=False) if abstract_md else ""
    )
    abstract_latex = cleanup_abstract_latex(abstract_latex)

    preamble = PREAMBLE.read_text(encoding="utf-8")
    title_page = build_title_page(abstract_latex)
    document = build_document(preamble, title_page, latex_body)
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
