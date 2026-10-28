#!/usr/bin/env bash
set -euo pipefail
mkdir -p app/src/main/assets
curl --fail --location --retry 3 --output app/src/main/assets/three.module.js https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js
curl --fail --location --retry 3 --output app/src/main/assets/THREE-LICENSE.txt https://raw.githubusercontent.com/mrdoob/three.js/r170/LICENSE
