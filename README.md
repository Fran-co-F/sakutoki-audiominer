# Sakutoki Audio Miner

Audio extraction and preview tool for Sakutoki dialogue files with AnkiConnect integration.

## Features

* **Fuzzy Search:** Non-exact string matching for dialogue retrieval using \`RapidFuzz\`.
* **Path Management:** Dynamic configuration for script and voice directories via \`settings.json\`.
* **Anki Integration:** Automated audio injection into Anki notes (supports specific Note IDs or last added note).
* **Multi-platform Core:** Python-based logic compatible with Linux and Windows.

## Requirements

The following dependencies are required:

```bash
pip install flet rapidfuzz just_playback requests
```

Linux users may require \`libasound2-dev\` or distribution-specific GStreamer payloads for audio playback also zenity and xdg-desktop-portal for folder selection.

## Build Instructions

To generate a standalone binary on Linux:

```bash
flet build linux --module-name script.py --project sakutoki-audiominer
```

The executable is generated in the \`build/linux\` directory.

## Directory Structure

The application expects the following directory layout (configurable via settings):

* **Scripts Folder:** Contains game dialogue files (.txt or .lua).
* **Voice Folder:** Must contain a \`vo/\` sub-directory with organized audio files.

## Status

* **Tested Environment:** Linux.
* **Windows Support:** Base code compatible; requires native compilation on Windows host.
* **AnkiConnect:** Requires Anki to be running with the AnkiConnect add-on enabled.
