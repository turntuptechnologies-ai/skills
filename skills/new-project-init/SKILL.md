---
name: new-project-init
description: 新しいプロジェクト/リポジトリを共通規約で立ち上げるとき。「新しいプロジェクトを作る」「リポジトリを初期化」「CLAUDE.md を用意」等で使う。フェーズ制・Conventional Commits・Issue→PR フローを定めた CLAUDE.md と基本ファイルを整える。stack 固有の雛形は scaffold-* Skill に任せる。
---

# 新規プロジェクト立ち上げ

新しいプロジェクトを、チーム共通の規約で初期化する。stack に依存しない土台を整える（言語固有のボイラープレートは `scaffold-*` Skill が担当）。

## 手順

1. **基本情報を確認する** — プロジェクト名 / 概要 / 主要言語・フレームワーク / 公開予定（private/public）/ ライセンス。不明なら聞く。

2. **CLAUDE.md を作る** — 同梱の [`CLAUDE.template.md`](CLAUDE.template.md) をコピーし、`{{ }}` プレースホルダを埋める。
   - 当てはまらないセクション（DB なし等）は削除してよい。
   - フェーズは新規なら通常 **PROTOTYPE**。
   - Agent Teams で進める方針なら、チーム体制・作業方式のセクションを追記する。

3. **基本ファイルを用意する**
   - `.gitignore`（言語に合わせる。生成物・`.env`・`node_modules` 等を除外）
   - `README.md`（概要・セットアップ・使い方の骨子）
   - `LICENSE`（public 予定なら。permissive 推奨＝MIT/Apache-2.0 等）
   - `.env.example`（秘密情報は実値を入れない）

4. **Git/GitHub をセットアップする**
   - `git init` → 初期コミット。デフォルトブランチは `main`。
   - リモートを作る場合は希望の可視性で（迷うなら **private 始まり**を推奨。公開は準備が整ってから）。
   - main 直 push を避ける運用にする（保護設定はリポジトリ管理者が後で有効化）。

5. **最初の作業から運用フローに乗せる** — 以降の変更は Issue → ブランチ → PR。
   品質チェックは `pre-pr-checks`、PR 作成は `create-pr` Skill を使う。

## 規約（テンプレに含まれる中身）

- **フェーズ制**: PROTOTYPE → ALPHA/BETA → PREVIEW → STABLE。
- **Conventional Commits**: `feat`/`fix`/`docs`/`refactor`/`test`/`chore`/`perf`。
- **開発フロー**: Issue → `issue-<番号>/<説明>` ブランチ → PR（`Closes #N`）→ squash merge → ブランチ削除。**main 直 push 禁止**。
- **ライセンス**: GPL 系の依存は避け、permissive を使う。
- **環境**: sudo 不使用、ツールは mise、ミドルウェアは Docker。

## ルール・コツ

- **公開を見据えるなら最初から秘密情報・固有情報を入れない。** `.env` はコミットしない、`.env.example` のみ。
- ライセンス方針は後で変えにくい。public 予定なら最初に決める。
- フェーズ名はプロジェクトの世界観に合わせて変更してもよい（相談されたら一緒に考える）。

## 補足

- この Skill 自体は汎用。特定の組織・社内リポジトリに依存しない。
