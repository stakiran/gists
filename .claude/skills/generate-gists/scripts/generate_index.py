"""docs/ 内の Gist ファイルに基づき index.md を生成する。

前提: index_entries.json に各 gist のメタ情報 (emoji, description) が格納されている。
オプション:
  --init  index_entries.json を生成・更新する（空の emoji/description エントリを追加）
  (なし)  index_entries.json をもとに docs/index.md を生成する
"""

import json
import os
import subprocess
import sys


DOCS_DIR = "docs"
ENTRIES_FILE = "index_entries.json"


def get_gist_meta_from_api():
    """APIから全gistのメタ情報(id, created_at, description)を取得する。"""
    metas = []
    page = 1
    while True:
        result = subprocess.run(
            ["gh", "api", f"users/stakiran/gists?per_page=100&page={page}",
             "--jq", '[.[] | {id, description, created_at}]'],
            capture_output=True, text=True, check=True,
        )
        output = result.stdout.strip()
        if not output or output == "[]":
            break
        metas.extend(json.loads(output))
        page += 1
    return metas


def init_entries():
    """index_entries.json を生成・更新する。既存エントリの emoji/description は保持。"""
    existing = {}
    if os.path.isfile(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r", encoding="utf-8") as f:
            for entry in json.load(f):
                existing[entry["id"]] = entry

    # docs/ に存在する gist ID を収集
    doc_ids = set()
    if os.path.isdir(DOCS_DIR):
        for fname in os.listdir(DOCS_DIR):
            if fname.endswith(".md") and fname != "index.md":
                doc_ids.add(fname[:-3])

    # API からメタ情報取得
    metas = get_gist_meta_from_api()

    entries = []
    for meta in metas:
        gist_id = meta["id"]
        if gist_id not in doc_ids:
            continue
        if gist_id in existing:
            entry = existing[gist_id]
            entry["created_at"] = meta["created_at"]
        else:
            entry = {
                "id": gist_id,
                "created_at": meta["created_at"],
                "emoji": "",
                "description": meta.get("description") or "",
            }
        entries.append(entry)

    # created_at 降順
    entries.sort(key=lambda e: e["created_at"], reverse=True)

    with open(ENTRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    empty_count = sum(1 for e in entries if not e["emoji"] or not e["description"])
    print(f"Updated {ENTRIES_FILE}: {len(entries)} entries ({empty_count} need emoji/description)")


def generate_index():
    """index_entries.json をもとに docs/index.md を生成する。"""
    if not os.path.isfile(ENTRIES_FILE):
        print(f"Error: {ENTRIES_FILE} not found. Run with --init first.", file=sys.stderr)
        sys.exit(1)

    with open(ENTRIES_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)

    lines = [
        "# My Gists",
        "[stakiran's gists](https://gist.github.com/stakiran)",
        "",
        "| No | Emoji |  |",
        "| --- | --- | --- |",
    ]

    for entry in entries:
        created = entry["created_at"].replace("T", " ").replace("Z", "")
        emoji = entry.get("emoji", "")
        desc = entry.get("description", "")
        link = f"[{desc}]({entry['id']}.md)"
        lines.append(f"| {created} | {emoji} | {link} |")

    os.makedirs(DOCS_DIR, exist_ok=True)
    path = os.path.join(DOCS_DIR, "index.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated: {path} ({len(entries)} entries)")


def main():
    if "--init" in sys.argv:
        init_entries()
    else:
        generate_index()


if __name__ == "__main__":
    main()
