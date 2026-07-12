#!/usr/bin/env bash
# SessionStart(clear|compact) で、プロジェクトの引き継ぎ書があればコンテキストに注入する。
# 無ければ何も出力せず静かに終わる（handoff Skill を使っていないプロジェクトに影響しない）。
set -euo pipefail

project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
handoff_file="$project_dir/.claude/handoff/latest.md"

[ -f "$handoff_file" ] || exit 0

echo "[turntup:handoff] 前セッションの引き継ぎ書が見つかりました（.claude/handoff/latest.md）。"
echo "保存時点からコードが変わっている可能性があるため、Git 状態（ブランチ・未コミット変更）を照合してから使うこと。"
echo "ユーザーがこの作業の続きを指示したら「次の一手」から再開する。無関係な指示ならこの引き継ぎ書は無視してよい。"
echo "---"
# 巨大ファイルでコンテキストを食い潰さないよう上限を設ける（Skill 側の目安は 100 行以内）
head -c 16000 "$handoff_file"
