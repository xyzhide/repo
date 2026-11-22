#!/usr/bin/env bash
# PostToolUse フック: 編集後に lint → build の順で、定義されているものだけ実行する。
#
# - package.json が無い、または lint / build が定義されていない場合は何もせず終了する（exit 0）。
# - 実行して失敗した場合は exit 2 にし、出力を Claude に返して直させる。
# - 依存のインストールは行わない（node_modules が無い場合は失敗として報告する）。

set -u

HOOKS_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" || exit 0

if [ ! -f package.json ]; then
  echo "post-edit-check: package.json が無いため lint/build はスキップしました。" >&2
  exit 0
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "post-edit-check: npm が見つからないため lint/build はスキップしました。" >&2
  exit 0
fi

# package.json の scripts に lint / build があるかを判定する。
# Python が使えない場合は "no" 扱いになり、安全側（実行しない）に倒れる。
has_script() {
  [ "$(bash "$HOOKS_DIR/run-python.sh" "$HOOKS_DIR/has-script.py" "$1" 2>/dev/null)" = "yes" ]
}

run_script() {
  local name="$1"
  echo "post-edit-check: npm run ${name} を実行します。" >&2
  local out
  if out=$(npm run "$name" --silent 2>&1); then
    echo "post-edit-check: ${name} 成功。" >&2
    return 0
  fi
  echo "post-edit-check: ${name} が失敗しました。出力:" >&2
  echo "$out" | tail -n 60 >&2
  return 1
}

if has_script lint; then
  run_script lint || exit 2
  exit 0
fi

if has_script build; then
  run_script build || exit 2
  exit 0
fi

echo "post-edit-check: package.json に lint / build が無いためスキップしました。" >&2
exit 0
