# INIT.md — 新しいセッションの開始手順

長時間の作業を、毎回同じ状態から再開するための手順です。上から順に行います。

## 1. 読む（変更はまだしない）

1. `CLAUDE.md` — 目的、絶対ルール、進め方、公開前チェック
2. `feature_list.json` — 完了している項目と、未完了の項目
3. `claude-progress.txt` — 直近の作業ログと、未了の次の一手

## 2. 状態を確認する

- ファイルの存在: `CLAUDE.md`、`.claude/settings.json`、`.claude/skills/`、`.claude/agents/`、`.claude/hooks/`
- 設定 JSON の妥当性: `python3 -c 'import json;json.load(open(".claude/settings.json"))'`
- 秘密情報ブロックの動作: 次のコマンドは exit 2 で終わること（テスト値は組み立てて作るので、このファイルに秘密情報の形そのものは残らない）

  ```bash
  K="IOSFODNN7EXAMPLE"
  echo "{\"tool_input\":{\"file_path\":\"/tmp/x.md\",\"content\":\"key=AKIA${K}\"}}" | python3 .claude/hooks/block-secrets.py; echo "exit=$?"
  ```

- MCP の状態: `claude mcp list`（21st の登録状況を確認する）
- build / lint: `package.json` があれば `npm run lint` と `npm run build` を実行する。無ければ「未定義」と記録する。

## 3. 作業を選ぶ

- `feature_list.json` で `status` が `todo` または `in_progress` の項目から、1つだけ選ぶ。
- 対象が不明確なら、着手前にユーザーに確認する。

## 4. 作業する

- `site-build` スキルの手順に従い、1機能ずつ進める。
- 完了と言う前に、`pre-publish-check` などで確認した事実を残す。

## 5. 区切りで記録する

- `feature_list.json` の該当項目の `status` と `evidence` を更新する（ユーザーの確認を得た後のみ `passing`）。
- `claude-progress.txt` の先頭に、日付・作業内容・未了・次の一手を追記する。

## 注意

- sitetech.jp 本体には触れない。
- 外部送信、公開、デプロイは、ユーザーの明示的な指示と確認があるまで行わない。
- 秘密情報をこれらのファイルに書かない。
