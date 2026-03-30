"""指定した ID の Gist を取得し docs/{id}.md に書き込む。

使い方: python fetch_gist.py <gist_id> [<gist_id> ...]
"""

import os
import subprocess
import sys


def fetch_and_save(gist_id, docs_dir="docs"):
    result = subprocess.run(
        ["gh", "api", f"gists/{gist_id}", "--jq", ".files | to_entries[0].value.content"],
        capture_output=True, text=True, check=True, encoding="utf-8",
    )
    content = result.stdout
    os.makedirs(docs_dir, exist_ok=True)
    path = os.path.join(docs_dir, f"{gist_id}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_gist.py <gist_id> [<gist_id> ...]", file=sys.stderr)
        sys.exit(1)

    for gist_id in sys.argv[1:]:
        fetch_and_save(gist_id)


if __name__ == "__main__":
    main()
