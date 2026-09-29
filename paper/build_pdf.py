import markdown
import pathlib

src = pathlib.Path("paper.md").read_text(encoding="utf-8")

html_body = markdown.markdown(
    src,
    extensions=["tables", "fenced_code", "sane_lists", "footnotes", "toc", "attr_list"],
    extension_configs={"toc": {"permalink": False}},
)

css = """
@page { size: Letter; margin: 2.2cm 2cm; }
body {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 10.8pt;
  line-height: 1.45;
  color: #1a1a1a;
  max-width: 100%;
}
h1 { font-size: 18pt; margin-top: 1.6em; page-break-before: always; }
body > h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14pt; margin-top: 1.4em; border-bottom: 1px solid #ccc; padding-bottom: 0.15em; }
h3 { font-size: 12pt; margin-top: 1.2em; }
h4 { font-size: 11pt; margin-top: 1em; }
p, li { orphans: 3; widows: 3; }
code, pre {
  font-family: "Consolas", "Menlo", monospace;
  font-size: 9pt;
  background: #f4f4f4;
}
pre {
  padding: 0.6em 0.8em;
  border: 1px solid #ddd;
  border-radius: 3px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 9.5pt;
}
th, td {
  border: 1px solid #999;
  padding: 4px 7px;
  text-align: left;
  vertical-align: top;
}
th { background: #eee; }
img {
  max-width: 100%;
  display: block;
  margin: 0.8em auto;
  border: 1px solid #ccc;
}
blockquote {
  border-left: 3px solid #ccc;
  margin: 0.8em 0;
  padding: 0.2em 1em;
  color: #444;
}
em { color: #333; }
a { color: #114488; text-decoration: none; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.6em 0; }
"""

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Storing, Displaying, and Querying Building Analytics on IFC Models</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

pathlib.Path("paper.html").write_text(html, encoding="utf-8")
print("wrote paper.html", len(html), "bytes")
