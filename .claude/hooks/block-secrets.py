#!/usr/bin/env python3
"""PreToolUse フック: 秘密情報らしい文字列を含む書き込みを止める。

stdin の JSON から書き込み内容を取り出して検査する。
該当があれば stderr に理由を出し、exit 2 で書き込みをブロックする。
JSON が読めない場合は、フック自体の不具合で作業を止めないよう exit 0 にする。
"""
import json
import re
import sys

PATTERNS = [
    ("AWS アクセスキー", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("秘密鍵ブロック", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("sk 形式の API キー", re.compile(r"sk-(ant-)?[A-Za-z0-9_\-]{20,}")),
    ("GitHub トークン", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("Slack トークン", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Google API キー", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    (
        "代入形式の秘密値",
        re.compile(
            r"(?i)(api[_-]?key|secret|passwd|password|token|access[_-]?key)"
            r"\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
        ),
    ),
]

# .env 本体の書き込みは禁止。.env.example 等のひな形は許可する。
SECRET_FILE = re.compile(r"(^|/)\.env(\.[A-Za-z0-9_-]+)?$")
TEMPLATE_FILE = re.compile(r"\.env\.(example|sample|template)$")


def written_text(tool_input):
    """書き込まれる新しい内容だけを集める（古い内容は対象外）。"""
    parts = []
    if isinstance(tool_input.get("content"), str):
        parts.append(tool_input["content"])
    if isinstance(tool_input.get("new_string"), str):
        parts.append(tool_input["new_string"])
    for edit in tool_input.get("edits", []) or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            parts.append(edit["new_string"])
    return "\n".join(parts)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""

    if SECRET_FILE.search(file_path) and not TEMPLATE_FILE.search(file_path):
        print(
            f"ブロック: {file_path} は秘密情報を入れる .env 本体です。"
            "置き場所の手順だけを書き、値は環境変数やシークレット機能に置いてください。",
            file=sys.stderr,
        )
        return 2

    text = written_text(tool_input)
    for label, pattern in PATTERNS:
        if pattern.search(text):
            print(
                f"ブロック: 秘密情報らしい文字列（{label}）を検出しました。"
                f"対象: {file_path or '(不明)'}。"
                "値を削除するか、プレースホルダに置き換えてください。",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
