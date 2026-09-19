"""Assemble the NRC-styled report from nrc-style/*.md and render it to PDF.

Concatenates the part files in order, rewrites figure paths to be relative to
this folder, writes nrc-style-paper.md and .html, then prints the HTML to
nrc-style-paper.pdf with headless Chrome.
"""

import pathlib
import subprocess
import markdown

HERE = pathlib.Path(__file__).parent
PARTS = [
    "p00-front.md",
    "p01-background.md",
    "p05-storage.md",
    "p06-display.md",
    "p07-agent.md",
    "p08-poc.md",
    "p09-limitations.md",
    "p10-future.md",
    "p11-roadmap.md",
    "p12-refs.md",
    "p13-annexes.md",
]

src = "\n".join((HERE / "nrc-style" / p).read_text(encoding="utf-8") for p in PARTS)
src = src.replace("](../figures/", "](figures/")
(HERE / "nrc-style-paper.md").write_text(src, encoding="utf-8")

html_body = markdown.markdown(
    src,
    extensions=["tables", "fenced_code", "sane_lists", "footnotes", "toc", "attr_list", "md_in_html"],
    extension_configs={"toc": {"permalink": False}},
)

css = """
@page { size: Letter; margin: 2.2cm 2cm 2.0cm 2cm; }
body {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 10.5pt;
  line-height: 1.5;
  color: #111;
}

/* Front matter pages, each on its own sheet. */
.coverpage, .titlepage, .signaturepage, .blankpage { page-break-after: always; }
.coverpage { font-size: 8.5pt; color: #333; line-height: 1.35; }
.coverpage p { margin: 0.5em 0; }
.titlepage { text-align: center; padding-top: 5cm; }
.titlepage h1 { font-size: 20pt; page-break-before: avoid; margin-bottom: 1.6em; border: none; }
.titlepage p { margin: 0.45em 0; }
.signaturepage { padding-top: 2cm; }
.signaturepage table { width: 60%; font-size: 10pt; }
.blankpage { padding-top: 10cm; text-align: center; color: #666; font-style: italic; }

h1 {
  font-size: 15pt;
  margin-top: 1.6em;
  page-break-before: always;
  page-break-after: avoid;
  border-bottom: 1.5px solid #333;
  padding-bottom: 0.2em;
}
.coverpage + h2, body > h2:first-of-type { page-break-before: avoid; }
h2 { font-size: 12.5pt; margin-top: 1.5em; page-break-after: avoid; }
h3 { font-size: 11pt; margin-top: 1.2em; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin-top: 1em; page-break-after: avoid; font-style: italic; }

p, li { orphans: 3; widows: 3; text-align: justify; }

code, pre { font-family: "Consolas", "Menlo", monospace; font-size: 8.8pt; background: #f5f5f5; }
pre {
  padding: 0.6em 0.8em;
  border: 1px solid #ddd;
  white-space: pre-wrap;
  word-wrap: break-word;
  page-break-inside: avoid;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.4em 0 1.2em 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
th, td { border: 1px solid #888; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #ececec; }

/* Table captions: the bold "Table N" paragraph that precedes each table. */
p > strong:first-child { }

img { max-width: 92%; display: block; margin: 1em auto 0.3em auto; border: 1px solid #bbb; }

/* Figure captions: the italic paragraph that follows each image. */
p > em:only-child {
  display: block;
  font-size: 9pt;
  text-align: left;
  margin: 0 auto 1.4em auto;
  max-width: 92%;
  color: #222;
}

blockquote { border-left: 3px solid #ccc; margin: 0.8em 0; padding: 0.2em 1em; color: #444; }
a { color: #113366; text-decoration: none; word-break: break-all; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.6em 0; }
"""

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Storing, displaying, and querying building analytics on IFC models with a large language model agent layer</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_path = HERE / "nrc-style-paper.html"
html_path.write_text(html, encoding="utf-8")
print("wrote", html_path.name, len(html), "bytes")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf_path = HERE / "nrc-style-paper.pdf"
subprocess.run(
    [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ],
    check=True,
)
print("wrote", pdf_path.name, pdf_path.stat().st_size, "bytes")
