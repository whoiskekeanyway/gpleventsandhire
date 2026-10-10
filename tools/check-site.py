"""Site sanity check — run before every commit:  python3 tools/check-site.py

Checks every tracked HTML page is complete, JSON-LD parses, local links and
images resolve, and every sitemap URL is a live, indexable page.
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

files = [f for f in subprocess.check_output(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.html"]).decode().split()
    if os.path.exists(f) and not f.startswith("tools/")]
problems = []

for f in files:
    s = open(f, encoding="utf-8").read()
    if len(s) < 2000 or not s.rstrip().endswith("</html>"):
        problems.append(("INCOMPLETE PAGE", f))
    if "item-template" in f:
        continue
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            problems.append(("BAD JSON-LD", f, str(e)))
    for m in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']', s):
        url = m.group(1)
        if re.match(r"(https?:|mailto:|tel:|data:|javascript:)", url) or url.startswith("#") or url == "/":
            continue
        path = url.split("#")[0].split("?")[0]
        base = "." if path.startswith("/") else os.path.dirname(f)
        if path and not os.path.exists(os.path.normpath(os.path.join(base, urllib.parse.unquote(path.lstrip("/"))))):
            problems.append(("BROKEN LINK", f, url))

sitemap = open("sitemap.xml", encoding="utf-8").read()
if sitemap.count("<url>") != sitemap.count("<loc>"):
    problems.append(("SITEMAP", "<url> without <loc>"))
for u in re.findall(r"<loc>\s*https://www\.gpleventsandhire\.co\.za/([^<\s]*)\s*</loc>", sitemap):
    page = u or "index.html"
    if not os.path.exists(page):
        problems.append(("SITEMAP MISSING PAGE", page))
    elif 'content="noindex' in open(page, encoding="utf-8").read():
        problems.append(("SITEMAP NOINDEX PAGE", page))

json.load(open("hire-items.json", encoding="utf-8"))

# The CSS bundle must be rebuilt after any stylesheet edit (python3 tools/build-css.py)
import glob
bundle_time = os.path.getmtime("css/site.css")
for css in glob.glob("css/*.css"):
    if not css.endswith("site.css") and os.path.getmtime(css) > bundle_time + 1:
        problems.append(("CSS BUNDLE STALE", css, "run python3 tools/build-css.py"))

for p in problems:
    print(*p)
print(f"{len(files)} pages checked, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
