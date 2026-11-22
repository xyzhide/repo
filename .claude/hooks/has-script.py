#!/usr/bin/env python3
"""カレントの package.json の scripts に、指定名があるかを判定する。

使い方: run-python.sh has-script.py <scriptName>
結果を stdout に "yes" または "no" で出す。
"""
import json
import sys

try:
    scripts = json.load(open("package.json", encoding="utf-8")).get("scripts") or {}
except Exception:
    print("no")
    sys.exit(0)

print("yes" if len(sys.argv) > 1 and sys.argv[1] in scripts else "no")
