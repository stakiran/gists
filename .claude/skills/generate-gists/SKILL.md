---
name: generate-gists
description: stakiran の GitHub Gists を取得し docs/ に静的サイト用 Markdown を生成する
---

# Generate Gists Site

GitHub ユーザー "stakiran" の Gists を取得し、`docs/` ディレクトリに静的サイト用の Markdown ファイルを生成する。

スクリプトはすべて `.claude/skills/generate-gists/scripts/` にある。

## 手順

### 1. 取得対象の Gist ID 一覧を取得

```
python .claude/skills/generate-gists/scripts/list_gist_ids.py --diff
```

- `--diff` をつけると、既に `docs/` にあるものを除外して差分のみ出力する
- `--diff` なしで全 ID を出力する

### 2. Gist の内容を取得して docs/ に保存

```
python .claude/skills/generate-gists/scripts/fetch_gist.py <gist_id> [<gist_id> ...]
```

手順1で得た ID を渡して実行する。複数 ID を一度に指定できる。

### 3. index_entries.json の生成・更新

```
python .claude/skills/generate-gists/scripts/generate_index.py --init
```

`index_entries.json` に全 gist のエントリが作られる。`emoji` と `description` が空のエントリが未入力分。

### 4. index_entries.json の emoji と description を埋める

`index_entries.json` を読み、空の `emoji` と `description` があるエントリを抽出する。
件数が多い場合はバッチに分割し、Agent を並列で起動して処理する。

各 Agent への指示:
- 担当する gist ID のリストを渡す
- 各 gist の内容（`docs/{gist_id}.md`）を読んで emoji と description を判断する
  - `emoji`: 内容を最もよく表す絵文字を1つ
  - `description`: 内容を日本語で簡潔に表現（description があればベースにする）
- **Agent が `index_entries.json` を直接 Edit で書き換える**（シェル経由のデータ受け渡しを避けるため）

### 5. index.md の生成

```
python .claude/skills/generate-gists/scripts/generate_index.py
```

`index_entries.json` の内容をもとに `docs/index.md` を生成する。

### 6. 完了報告

新規取得した gist の件数、スキップした(既存の) gist の件数、および `docs/` 内の総ファイル数を報告する。
