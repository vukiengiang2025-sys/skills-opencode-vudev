#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from rich import print

from androguard.misc import AnalyzeAPK

TOOLS_DIR = os.environ.get('TOOLS_DIR', '/opt/tools')


def run_cmd(cmd, cwd=None, capture=False):
    print(f"[green]Running:[/green] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)
    if result.returncode != 0:
        print(f"[red]Command failed:[/red] {' '.join(cmd)}")
        print(result.stdout)
        print(result.stderr)
    return result


def run_apkid(apk_path):
    # apkid -j <apk>
    cmd = [sys.executable, '-m', 'apkid', '-j', apk_path]
    res = run_cmd(cmd, capture=True)
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"error": "apkid failed", "output": res.stdout + res.stderr}


def run_jadx(apk_path, out_dir):
    jadx_bin = Path(TOOLS_DIR) / 'jadx' / 'bin' / 'jadx'
    if not jadx_bin.exists():
        return {"error": "jadx not installed"}
    out = Path(out_dir) / 'jadx'
    out.mkdir(parents=True, exist_ok=True)
    cmd = [str(jadx_bin), '-d', str(out), apk_path]
    res = run_cmd(cmd, capture=True)
    return {"status": "ok"}


def run_apktool(apk_path, out_dir):
    apktool = Path(TOOLS_DIR) / 'apktool'
    if not apktool.exists():
        apktool = None
    name = Path(apk_path).stem
    dest = Path(out_dir) / name / 'apktool'
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [str(apktool), 'd', apk_path, '-o', str(dest), '-f'] if apktool else ['java', '-jar', str(Path(TOOLS_DIR)/'apktool.jar'), 'd', apk_path, '-o', str(dest), '-f']
    res = run_cmd(cmd, capture=True)
    return {"status": "ok", "path": str(dest)}


def run_androguard(apk_path):
    try:
        a, d, dx = AnalyzeAPK(apk_path)
        manifest = a.get_android_manifest_xml()
        perms = list(a.get_permissions())
        pkg = a.get_package()
        activities = list(a.get_activities())
        services = list(a.get_services())
        receivers = list(a.get_receivers())
        providers = list(a.get_providers())

        exported = []
        for comp in activities + services + receivers + providers:
            try:
                exported.append({"name": comp, "exported": a.is_exported(comp)})
            except Exception:
                exported.append({"name": comp, "exported": None})

        return {
            "package": pkg,
            "permissions": perms,
            "activities": activities,
            "services": services,
            "receivers": receivers,
            "providers": providers,
            "exported": exported,
        }
    except Exception as e:
        return {"error": str(e)}


def make_report(apk_path, out_dir):
    apk_path = str(Path(apk_path).resolve())
    name = Path(apk_path).stem
    dest = Path(out_dir) / name
    dest.mkdir(parents=True, exist_ok=True)

    report = {}
    report['apk'] = apk_path

    report['apkid'] = run_apkid(apk_path)

    report['androguard'] = run_androguard(apk_path)

    try:
        run_jadx(apk_path, out_dir)
        report['jadx_path'] = str(Path(out_dir) / 'jadx')
    except Exception as e:
        report['jadx_error'] = str(e)

    try:
        run_apktool(apk_path, out_dir)
        report['apktool_path'] = str(dest / 'apktool')
    except Exception as e:
        report['apktool_error'] = str(e)

    # Write JSON report
    report_path = dest / 'report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Simple HTML summary
    html = ['<html><head><meta charset="utf-8"><title>APK Report</title></head><body>']
    html.append(f"<h1>Report for {name}</h1>")
    html.append('<h2>APKiD</h2>')
    html.append('<pre>' + json.dumps(report.get('apkid'), indent=2, ensure_ascii=False) + '</pre>')
    html.append('<h2>Androguard</h2>')
    html.append('<pre>' + json.dumps(report.get('androguard'), indent=2, ensure_ascii=False) + '</pre>')
    html.append('</body></html>')
    with open(dest / 'report.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print(f"[green]Report written to {report_path} and {dest / 'report.html'}[/green]")
    return str(report_path)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')

    p = sub.add_parser('analyze')
    p.add_argument('apk', help='Path to APK to analyze')
    p.add_argument('-o', '--out', default='/work/out', help='Output directory')

    args = parser.parse_args()
    if args.cmd == 'analyze':
        apk = args.apk
        out = args.out
        make_report(apk, out)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
