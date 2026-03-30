---
name: generate-gists
description: stakiran の GitHub Gists を取得し docs/ に静的サイト用 Markdown を生成する
---

# Generate Gists Site

GitHub ユーザー "stakiran" の Gists を取得し、`docs/` ディレクトリに静的サイト用の Markdown ファイルを生成する。

## 手順

### 1. Gists の取得と docs/ への保存

Python スクリプトを実行する。

```
python fetch_gists.py
```

- 差分取得（既存ファイルはスキップ）がデフォルト
- `--all` オプションで全件再取得も可能
- 進捗は自動で表示される

### 2. index_entries.json の生成・更新

```
python generate_index.py --init
```

`index_entries.json` に全 gist のエントリが作られる。`emoji` と `description` が空のエントリが未入力分。

### 3. index_entries.json の emoji と description を埋める

`index_entries.json` を読み、空の `emoji` と `description` を埋める。

- gist の内容（docs/{gist_id}.md）を読んで判断する
- `emoji`: 内容を最もよく表す絵文字を1つ
- `description`: 内容を日本語で簡潔に表現（description があればベースにする）

### 4. index.md の生成

```
python generate_index.py
```

`index_entries.json` の内容をもとに `docs/index.md` を生成する。

### 5. 完了報告

新規取得した gist の件数、スキップした(既存の) gist の件数、および `docs/` 内の総ファイル数を報告する。
