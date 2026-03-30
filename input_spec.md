# このリポジトリについて
My Gists を取得し、静的ウェブサイトとして公開する。

## ディレクトリ構成
- docs/
    - index.md
        - トップページであり、すべての gist file の目次をつくる
    - XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.md
        - gist file。1 つの gist を表現したページ

## index.md
以下フォーマットで構成する。

```
# My Gists
[stakiran’s gists](https://gist.github.com/stakiran)

| No | Emoji |  |
| --- | --- | --- | 
| 投稿日付を yyyy-mm-dd hh:mm:ss で書く | gist の内容を絵文字1つで表現 | [gistの内容を一言で表現](gist fileへのリンク) |
| ... | ... | ... |
```

ただし日付の降順で表示すること。

## gist file
コンテンツは gist の中身のみとし、gist.md などのファイル名や front matter は一切書かないこと。
