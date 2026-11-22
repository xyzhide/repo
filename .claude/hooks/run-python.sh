#!/usr/bin/env bash
# フック用の Python 起動ラッパー。
# 使い方: bash run-python.sh <スクリプト> [引数...]
# python3 → python → py の順に、実際に動くインタープリタを探して exec する。
# Windows では python3 が「Microsoft Store の案内」だけのことがあるため、動作確認まで行う。
# 見つからない場合は、フックの不具合で作業を止めないよう exit 0 にする（その旨を stderr に出す）。

if [ $# -lt 1 ]; then
  echo "run-python: スクリプトのパスが必要です。" >&2
  exit 0
fi

script="$1"
shift

for cand in python3 python py; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c 'import sys' >/dev/null 2>&1; then
    exec "$cand" "$script" "$@"
  fi
done

echo "run-python: 使える Python（python3 / python / py）が見つからないため、このフックをスキップしました。" >&2
exit 0
