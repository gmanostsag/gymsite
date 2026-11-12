#!/usr/bin/env python3
"""Μετατρέπει το site/ σε επίπεδη έκδοση για ιδιωτική προεπισκόπηση στο claude.ai.

python3 tools/export_artifact.py <φάκελος-εξόδου>

- σχετικά links (pilates.html αντί για /pilates/)
- χάρτης ως link (η προεπισκόπηση δεν επιτρέπει iframes)
- noindex, ώστε να μη μετρά ως διπλότυπο του πραγματικού site
"""
import glob, os, re, shutil, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
DST = sys.argv[1]
os.makedirs(DST, exist_ok=True)
shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DST, "assets"), dirs_exist_ok=True)

def flat(path):
    p = path.strip("/")
    return "index.html" if p == "" else p.replace("/", "-") + ".html"

MAPS = "https://www.google.com/maps/search/?api=1&amp;query=Training+Station+Fitness+Peristeri"
for f in glob.glob(SRC + "/**/index.html", recursive=True):
    rel = os.path.relpath(os.path.dirname(f), SRC)
    rel = "/" if rel == "." else "/" + rel + "/"
    s = open(f, encoding="utf-8").read()
    s = re.sub(r'(href|src)="/assets/', r'\1="assets/', s)
    s = re.sub(r'href="(/[a-z0-9\-]*/?)(#[^"]*)?"', lambda m: f'href="{flat(m.group(1))}{m.group(2) or ""}"', s)
    s = re.sub(r'<div class="map-facade"><button class="btn" data-src="[^"]*">Εμφάνιση χάρτη</button></div>',
               f'<a class="map-facade" href="{MAPS}" target="_blank" rel="noopener"><span class="btn">Άνοιγμα στο Google Maps</span></a>', s)
    s = s.replace("alert('Προεπισκόπηση: εδώ συνδέεται η φόρμα του WordPress (π.χ. Contact Form 7).');return false",
                  "event.preventDefault();this.insertAdjacentHTML('beforeend','<p class=&quot;todo full&quot;>Προεπισκόπηση: η φόρμα δεν στέλνει. Στο live site συνδέεται με το WordPress.</p>');return false")
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, nofollow">', s)
    out = flat(rel)
    if out == "index.html":  # η κύρια σελίδα τυλίγεται αυτόματα σε <html><head><body>
        s = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*', '', s, flags=re.I)
        s = s.replace('</head>\n<body>', '').replace('</body>\n</html>', '')
        s = re.sub(r'<title>[^<]*</title>', '<title>Νέο site Training Station</title>', s, count=1)
    open(os.path.join(DST, out), "w", encoding="utf-8").write(s)
print("OK", sorted(x for x in os.listdir(DST) if x.endswith(".html")))
