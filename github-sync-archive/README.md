# GitHub Sync Archive

Created: 2026-08-06

This folder is a compact text-first archive for syncing the saved project context to GitHub.

## Contents

- `conversations/`: saved Codex conversation exports and thread backups.
- `markdown/`: project Markdown documents copied from the repository root, `docs/`, and `outputs/`.
- `skills/`: selected workflow skill folders used by this project.
- `agents/`: selected agent prompt files, including `theme-image-director-v3.6`.

## Included File Types

- Markdown: project notes, scripts, prompts, and conversation backups.
- JSON/YAML: lightweight skill or agent metadata.
- Small scripts: helper scripts that are part of selected skill folders.

## Ignored On Purpose

Large downloaded/generated media and cache folders are excluded from this archive and are covered by `.gitignore`, including:

- `downloads/`, `dwonleod/`, `download/`, `Downloads/`
- `video02_work/`, `video03_work/`, `analysis_frames/`, `video_frames/`, `subtitle_frames/`
- `tmp/`, `.tmp_video_analysis/`, `.tmp_skill_create/`, `.npm-cache/`, `node_modules/`
- Common large media/binary extensions such as `.mp4`, `.mov`, `.mkv`, `.mp3`, `.wav`, `.zip`, `.onnx`

Current archive size is about 1.2 MB and contains text/configuration files only.
