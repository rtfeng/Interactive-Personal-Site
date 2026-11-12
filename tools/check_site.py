"""Pre-deploy checks for the homepage. Fails the build if anything a visitor would hit is broken."""
import re, sys, pathlib, html.parser

root = pathlib.Path(__file__).resolve().parent.parent
page = (root / "index.html").read_text(encoding="utf-8")
errors = []

# 1. HTML parses and key sections exist
class P(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.ids = set()
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id": self.ids.add(v)
p = P(); p.feed(page)
for sec in ["guide", "about", "now", "publications", "teaching", "work", "service", "contact", "after-hours", "cv"]:
    if sec not in p.ids: errors.append(f"missing section #{sec}")

# 2. Every self-hosted PDF the page links to exists
m = re.search(r"const LOCAL_PDF = new Set\((\[.*?\])\);", page, re.S)
if not m: errors.append("LOCAL_PDF list not found")
else:
    for k in re.findall(r'"([^"]+)"', m.group(1)):
        f = root / "papers" / f"{k}.pdf"
        if not f.exists() or f.stat().st_size < 10_000: errors.append(f"missing or empty PDF: papers/{k}.pdf")

# 3. Paper keys are unique (they become anchors and PDF file names)
keys = re.findall(r'\{ c:"[a-z]+", k:"([^"]+)"', page)
if len(keys) != len(set(keys)): errors.append("duplicate paper keys")

# 4. In-page anchors used by the guide resolve
for href in set(re.findall(r'href: "#([a-z0-9-]+)"', page)):
    if href not in p.ids and not href.startswith("paper-") and not href.startswith("pubs-"):
        errors.append(f"guide link to missing anchor #{href}")

print(f"checked {len(keys)} papers, {len(p.ids)} ids")
if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print("all checks passed")
