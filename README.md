# Skill: OpenCode APK Analyzer

This repository contains a self-contained "skill" to analyze Android APK files. It combines multiple open-source tools (APKiD, JADX, Apktool, Androguard) into a single Dockerized application with a CLI and optional REST API.

Features
- Detect packers/obfuscators (APKiD)
- Static analysis via Androguard (manifest, permissions, exported components)
- Decompile via JADX (extract Java-like source)
- Decode resources via Apktool (resources, smali)
- Outputs JSON report + HTML summary + artifacts directory

Quick start (Docker)

1. Build the image:

   docker build -t opencode-apk-skill:latest .

2. Run analysis (CLI) and collect outputs in ./out:

   docker run --rm -v $(pwd)/out:/out opencode-apk-skill:latest analyze /work/input/app.apk -o /out

3. Run REST API server (optional):

   docker run --rm -p 5000:5000 -v $(pwd)/out:/out opencode-apk-skill:latest api

API endpoints:
- POST /analyze (multipart file upload field 'apk') -> returns JSON report and stores artifacts in /out

Files created by the skill:
- /out/<apk_basename>/report.json
- /out/<apk_basename>/report.html
- /out/<apk_basename>/jadx/ (decompiled sources)
- /out/<apk_basename>/apktool/ (decoded resources)

For full docs, see README in repository.
