---
name: test-gh
description: gh コマンドの動作確認を行う
---

# gh コマンドテスト

gh CLI が使える状態かどうかを確認する。以下を順番に実行し、結果を報告する。

## チェック項目

### 1. gh のインストール確認

```
gh --version
```

バージョンが表示されれば OK。コマンドが見つからなければインストールされていない。

### 2. 認証状態の確認

```
gh auth status
```

認証済みかどうか、どのアカウントでログインしているかを確認する。

### 3. API アクセスの確認

stakiran の公開 Gists を1件だけ取得してみる。

```
gh api "users/stakiran/gists?per_page=1" --jq '.[0] | {id, description, created_at}'
```

JSON が返れば API アクセスは正常。

## 報告

各チェック項目の結果を OK / NG で一覧表示する。NG がある場合は対処方法も提示する。
