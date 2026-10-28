# AnimStudio3D

Android prototype for creating short, procedural 3D character animation clips.

## Build the APK
1. Use JDK 17, Gradle 8.9, Node.js 20 and Python 3.
2. Run `scripts/vendor_three.sh` once to download Three.js r170 and its MIT license into the Android assets directory.
3. Run `python3 scripts/validate_web_assets.py`.
4. Run `gradle --no-daemon assembleDebug`.
5. The debug APK is written to `app/build/outputs/apk/debug/app-debug.apk`.

The GitHub Actions workflow performs these steps and uploads the debug APK artifact.

## Current prototype features
- Procedural low-poly 3D character and a single room scene.
- Idle, walk, turn, wave, talk, cup pickup, cup placement, pointing and happy actions.
- A timed 30-second storyboard preview.
- Dialogue text, device text-to-speech preview, subtitle overlay, character color controls, camera and speed controls.
- Project JSON save/load including dialogue, scene settings and added props.
- 30-second viewport recording as WebM when supported by the device WebView.

## Important limitations
This is not yet a professional, general-purpose animation suite. The character is procedurally generated and does not use a production-quality skeletal rig or motion-capture data. Dialogue TTS is preview-only and is not muxed into exported video. MP4 export, frame-accurate phoneme lip-sync, arbitrary scene construction, multiple characters, full object manipulation, and broad Android-device QA are not implemented. Export depends on MediaRecorder support. Static checks and a successful build do not replace installation and real-device testing.

The Three.js runtime is downloaded at build time and packaged locally, so the installed app can render its 3D scene without fetching Three.js at runtime.
