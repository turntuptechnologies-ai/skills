#!/usr/bin/env bash
# PreToolUse フック: main/master への直接 push をブロックする。
#
# 「main 直 push 禁止」のような“確実に止めたい”制約は、Skill 本文の指示
# （モデルの判断に委ねる）ではなくフックで担保するのが筋。
# このスクリプトを対象プロジェクトの .claude/hooks/ に置き、
# .claude/settings.json で PreToolUse / matcher "Bash" に配線する
# （配線例は同ディレクトリの settings.snippet.json を参照）。
#
# 動作: stdin から PreToolUse の JSON を受け取り、git push が main/master を
# 明示的に対象にしている場合は exit 2 でブロックする
# （exit 2 のとき stderr のメッセージがモデルに渡り、実行は中止される）。
#
# 限界: 「main に居る状態での bare な `git push`」はコマンド文字列だけからは
# 判定できない。最終的な保証は GitHub のブランチ保護で行うこと。本フックは
# 明示的な push（origin main / HEAD:main 等）を早期に止める二重防御。

set -eu

input="$(cat)"

# 実行されようとしているコマンドを取り出す（jq があれば堅牢に、無ければ raw）
if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
else
  cmd="$input"
fi

# git push 以外は許可
printf '%s' "$cmd" | grep -qiE 'git[[:space:]]+push' || exit 0

# main/master を明示的に対象にした push をブロック
if printf '%s' "$cmd" | grep -qiE '(origin[[:space:]]+(main|master)\b|:(refs/heads/)?(main|master)\b|\bHEAD:(main|master)\b)'; then
  echo "🚫 main/master への直接 push は禁止です。ブランチを切って PR を作成してください（create-pr Skill / branching ルール）。" >&2
  exit 2
fi

exit 0
