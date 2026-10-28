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
    'id="subtitle"', "import * as THREE from './three.module.js';", 'window.saveProject', 'window.loadProject',
    'window.exportVideo', 'window.speakDialogue',
    "new THREE.WebGLRenderer", "renderer.render(scene,camera)",
]
missing = [item for item in required if item not in html]
if missing:
    print("FAIL: required UI/runtime markers missing:")
    print("\n".join(" - " + item for item in missing))
    raise SystemExit(1)
vendor = Path('app/src/main/assets/three.module.js')
if not vendor.exists() or vendor.stat().st_size < 100000:
    raise SystemExit('FAIL: local Three.js runtime missing or unexpectedly small')
if not Path('app/src/main/assets/THREE-LICENSE.txt').exists():
    raise SystemExit('FAIL: Three.js license file missing')
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
# Check the scripted demo has a bounded 30-second timeline and the expected key actions.
storyboard_start = html.find('const storyboard=[')
storyboard_end = html.find('];', storyboard_start)
if storyboard_start < 0 or storyboard_end < 0:
    raise SystemExit('FAIL: storyboard definition missing')
storyboard_text = html[storyboard_start:storyboard_end]
segments = re.findall(r"\{start:(\d+),end:(\d+),action:'([a-z]+)'\}", storyboard_text)
if len(segments) < 8 or int(segments[0][0]) != 0 or int(segments[-1][1]) != 30:
    raise SystemExit('FAIL: storyboard does not cover the complete 30-second demo')
actions = {name for _, _, name in segments}
if not {'walk', 'turn', 'talk', 'pick', 'place', 'point', 'happy'}.issubset(actions):
    raise SystemExit('FAIL: storyboard is missing required animation actions')
if "scriptMode=true;lastScriptAction=''" not in html:
    raise SystemExit('FAIL: video export does not trigger storyboard mode')
main_path = Path('app/src/main/java/com/animstudio3d/MainActivity.java')
main_java = main_path.read_text(encoding='utf-8')
for marker in ['WebViewAssetLoader', 'AndroidBridge', 'onShowFileChooser', 'MediaStore.Downloads']:
    if marker not in main_java:
        raise SystemExit(f'FAIL: Android integration marker missing: {marker}')
print("PASS: required UI markers found")
print("PASS: 30-second storyboard and required actions found")
print("PASS: Android save/load bridge markers found")
print("PASS: module JavaScript syntax valid")
print("NOTE: this is static validation; it does not replace Android-device visual, interaction, or export testing.")
