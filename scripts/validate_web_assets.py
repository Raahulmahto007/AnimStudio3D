#!/usr/bin/env python3
"""Static checks for the WebView animation editor before APK packaging."""
from pathlib import Path
import re
import subprocess
import tempfile
import sys

html_path = Path("app/src/main/assets/index.html")
if not html_path.exists():
    raise SystemExit("FAIL: missing app HTML asset")
html = html_path.read_text(encoding="utf-8")
required = [
    'id="view"', 'id="composite"', 'id="dialogue"',
    'id="subtitle"', 'window.saveProject', 'window.loadProject',
    'window.exportVideo', 'window.speakDialogue',
    "new THREE.WebGLRenderer", "renderer.render(scene,camera)",
]
missing = [item for item in required if item not in html]
if missing:
    print("FAIL: required UI/runtime markers missing:")
    print("\n".join(" - " + item for item in missing))
    raise SystemExit(1)
scripts = re.findall(r'<script type="module">(.*?)</script>', html, re.S)
if len(scripts) != 1:
    raise SystemExit(f"FAIL: expected one module script, found {len(scripts)}")
with tempfile.NamedTemporaryFile("w", suffix=".mjs", encoding="utf-8", delete=False) as tmp:
    tmp.write(scripts[0])
    temp_path = Path(tmp.name)
try:
    result = subprocess.run(["node", "--check", str(temp_path)], text=True, capture_output=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit("FAIL: JavaScript syntax validation")
finally:
    temp_path.unlink(missing_ok=True)
print("PASS: required UI markers found")
print("PASS: module JavaScript syntax valid")
print("NOTE: this is static validation; it does not replace Android-device visual, interaction, or export testing.")
