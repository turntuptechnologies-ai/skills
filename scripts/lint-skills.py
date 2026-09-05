#!/usr/bin/env python3
"""skills/*/SKILL.md の機械検査（skill-lint チェックリストの機械化可能部分）。

CI（.github/workflows/ci.yml）とローカル（`python3 scripts/lint-skills.py`）で実行する。
判断が要る項目（description のトリガー品質・完了条件の実質的な検証可能性・固有情報・
コマンドの実行検証（#10）・過剰指示（#11））は skill-lint Skill（モデルによる点検）の担当で、本スクリプトは扱わない。

検査項目（skill-lint チェックリストの対応番号）:
  - frontmatter の name がディレクトリ名と一致する（#1）
  - frontmatter の description が空でない（#2 の機械判定できる範囲）
  - 必須節（手順 / ルール・コツ / 完了条件）が存在する（#3）
  - 完了条件の前文（満たせない項目は黙って省略せず理由を報告）がある（#5）
  - 完了条件の節に曖昧語（適切に・十分に・ちゃんと）が無い（#4 の機械判定できる範囲）
  - README のカタログ表と skills/ ディレクトリが双方向に同期している（#7）
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"

REQUIRED_SECTIONS = ("## 手順", "## ルール・コツ", "## 完了条件")
PREAMBLE = "満たせない項目があれば、黙って省略せず理由を報告する"
VAGUE_WORDS = re.compile(r"適切に|十分に|ちゃんと")
# カタログ表の行（2 列目がバッククォートで囲まれた Skill 名）だけにマッチする
CATALOG_ROW = re.compile(r"^\|[^|]+\| `([a-z][a-z0-9-]*)` \|", re.MULTILINE)

errors: list[str] = []


def err(path: object, message: str) -> None:
    errors.append(f"{path}: {message}")


def strip_code_fences(text: str) -> str:
    """フェンス付きコードブロックを除去する。

    テンプレ例のフェンス内に `## 手順` 等の見出しを含む Skill（create-issue / create-pr /
    handoff 等）があるため、節の検出はフェンスを除いた本文に対して行う。
    前提: 3 連バッククォート + LF 改行のフェンスのみ対応（`~~~`・4 連・CRLF は対象外）。
    """
    return re.sub(r"(?ms)^[ \t]*```.*?^[ \t]*```[ \t]*$\n?", "", text)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def section_body(text: str, heading: str) -> str | None:
    """heading で始まる節の本文（次の `## ` 見出しまで）。見出しが無ければ None。"""
    pattern = rf"^{re.escape(heading)}[^\n]*$\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else None


def check_skill(skill_dir: Path) -> None:
    md = skill_dir / "SKILL.md"
    rel = md.relative_to(ROOT)
    if not md.is_file():
        err(skill_dir.relative_to(ROOT), "SKILL.md が無い")
        return
    text = md.read_text(encoding="utf-8")

    fm = parse_frontmatter(text)
    if fm is None:
        err(rel, "frontmatter（--- ... ---）が無い")
    else:
        if fm.get("name") != skill_dir.name:
            err(rel, f"frontmatter の name「{fm.get('name')}」がディレクトリ名「{skill_dir.name}」と一致しない")
        if not fm.get("description"):
            err(rel, "frontmatter の description が空")

    # 節の検出はフェンス内の見出し（テンプレ例）を誤認しないよう、フェンス除去後の本文で行う
    body = strip_code_fences(text)

    # 節名は前方一致（例: 「## 手順（保存）」も「## 手順」の節として扱う）
    for heading in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(heading)}", body, re.MULTILINE):
            err(rel, f"必須節が無い: {heading}")

    done = section_body(body, "## 完了条件")
    if done is not None:
        if PREAMBLE not in done:
            err(rel, f"完了条件の前文（「{PREAMBLE}」）が無い")
        for m in VAGUE_WORDS.finditer(done):
            err(rel, f"完了条件に曖昧語「{m.group(0)}」がある")


def check_catalog(skill_names: set[str]) -> None:
    if not README.is_file():
        err("README.md", "ファイルが無い")
        return
    catalog = set(CATALOG_ROW.findall(README.read_text(encoding="utf-8")))
    for name in sorted(skill_names - catalog):
        err("README.md", f"カタログ表に `{name}` の行が無い")
    for name in sorted(catalog - skill_names):
        err("README.md", f"カタログ表の `{name}` に対応する skills/{name}/ が無い")


def main() -> int:
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    for skill_dir in skill_dirs:
        check_skill(skill_dir)
    check_catalog({d.name for d in skill_dirs})

    if errors:
        print(f"skill-lint (mechanical): {len(errors)} 件のエラー")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"skill-lint (mechanical): OK（{len(skill_dirs)} Skill、README カタログ同期済み）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
