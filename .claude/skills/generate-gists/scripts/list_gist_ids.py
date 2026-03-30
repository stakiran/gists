"""stakiran の公開 Gists の ID 一覧を取得する。

出力: 1行1IDで標準出力に出力
オプション: --diff  既に docs/ にあるものを除外する
"""

import json
import os
import subprocess
import sys


def fetch_all_gist_ids():
    ids = []
    page = 1
    while True:
        result = subprocess.run(
            ["gh", "api", f"users/stakiran/gists?per_page=100&page={page}", "--jq", ".[].id"],
            capture_output=True, text=True, check=True,
        )
        output = result.stdout.strip()
        if not output:
            break
        ids.extend(output.splitlines())
        page += 1
    return ids


def main():
    diff_mode = "--diff" in sys.argv
    docs_dir = "docs"

    ids = fetch_all_gist_ids()

    for gist_id in ids:
        if diff_mode and os.path.isfile(os.path.join(docs_dir, f"{gist_id}.md")):
            continue
        print(gist_id)


if __name__ == "__main__":
    main()
