<!--
作る前に: これは本当に「Skill」向きか？（→ ../README.md「Skill と他の操縦手段」）
  - 呼び出して使う手順（procedure）            → Skill（このテンプレ）
  - 常に守る制約（〜してはいけない / 〜であること）→ Rules（.claude/rules/。paths でスコープ可）
  - モデルの判断を介さず確実に走らせる/止める   → Hook（.claude/settings.json の PreToolUse 等）
  - 別コンテキストで調査して結果だけ返したい     → Subagent（.claude/agents/）
Skill だと確定したら、この説明コメントごと中身を書き換える。
-->
---
name: skill-name
description: いつこの Skill を使うか・何をするかを一文で。name と description だけは常時ロードされ（progressive disclosure）、Claude はこれを読んで発動可否を判断する。だから「どんな状況・どんな指示で使うか」のトリガーを具体的に書く。例) "PR を作成するとき。「PR 作って」等で発動。ブランチを切り、Conventional Commits タイトルとテンプレ本文で PR を作成する。"
---

# <Skill のタイトル>

## このスキルがやること

<何を達成するスキルか、1〜2 行で>

## 手順

1. <ステップ 1>
2. <ステップ 2>
3. <ステップ 3>

## ルール・コツ

- <守ってほしい制約>
- <ありがちな失敗とその回避>
- <他の Skill / Rules / Hook と連携するなら、その関係>

## 補足

- 社内固有情報（社名・内部 URL・認証情報など）は書かない。環境差は引数や環境変数で受け取る。
- 「毎回必ず実行/ブロックしたい」処理が出てきたら、それは Skill ではなく Hook に切り出す。
