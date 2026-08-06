---
name: new-project-init
description: 新しいプロジェクト/リポジトリを共通規約で立ち上げるとき。「新しいプロジェクトを作る」「リポジトリを初期化」「CLAUDE.md を用意」等で使う。フェーズ制・Conventional Commits・Issue→PR フローを定めた CLAUDE.md、常時効かせる Rules、main 保護フックなど基本ファイルを整える。stack 固有の雛形は scaffold-* Skill に任せる。
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

4. **Rules を撒く** — 同梱の [`rules/`](rules/) を対象プロジェクトの `.claude/rules/` にコピーする。
   - `commit-conventions.md` / `license-policy.md` / `no-secrets.md` / `branching.md`。
   - Rules は「**常に守る制約**」。CLAUDE.md（概要・手順）とは役割が別。詳細な制約は Rules を正とし、CLAUDE.template 側では重複させない。
   - 特定パスにだけ効かせたい制約は、frontmatter に `paths:` を足してスコープする（トークン節約）。

5. **main 保護フックを撒く** — 同梱の [`hooks/block-main-push.sh`](hooks/) を `.claude/hooks/` に置き（`chmod +x`）、[`hooks/settings.snippet.json`](hooks/) を `.claude/settings.json` の `hooks.PreToolUse` にマージする。
   - 「main 直 push 禁止」のような**ハードガードは指示文ではなくフックで担保**する（モデルの判断に委ねない）。
   - 最終的な保証は GitHub のブランチ保護。フックは早期に止める二重防御。

6. **Git/GitHub をセットアップする**
   - `git init` → 初期コミット。デフォルトブランチは `main`。
   - リモートを作る場合は希望の可視性で（迷うなら **private 始まり**を推奨。公開は準備が整ってから）。
   - リポジトリ管理者がブランチ保護を有効化する。public で公開する（または後から公開に切り替える）際は、`repo-publish-security` Skill で公開時のセキュリティ設定（secret scanning・ブランチ保護 ruleset・Actions 権限等）を点検・適用する。

7. **最初の作業から運用フローに乗せる** — 以降の変更は Issue → ブランチ → PR。
   品質チェックは `pre-pr-checks`、PR 作成は `create-pr` Skill を使う。

## 操縦手段の使い分け

この Skill が撒くものは、Claude Code の操縦手段ごとに役割が分かれている（[参考](../../README.md#参考--references)）。

- **CLAUDE.md**（`CLAUDE.template.md`）= プロジェクト概要・構成・手順。常時ロード。
- **Rules**（`rules/`）= 常に守る制約（Conventional Commits / ライセンス / 秘密情報 / ブランチ運用）。必要時ロード、`paths:` でスコープ可。
- **Hook**（`hooks/`）= 確実に止めたいハードガード（main 直 push ブロック）。モデルの判断を介さない。
- **Skill**（`pre-pr-checks` / `create-pr` / `scaffold-*`）= 呼び出して使う手順。

補足: フェーズ制（PROTOTYPE→STABLE）、環境ルール（sudo 不使用・mise・Docker）は CLAUDE.template に含む。

## ルール・コツ

- **公開を見据えるなら最初から秘密情報・固有情報を入れない。** `.env` はコミットしない、`.env.example` のみ。
- ライセンス方針は後で変えにくい。public 予定なら最初に決める。
- フェーズ名はプロジェクトの世界観に合わせて変更してもよい（相談されたら一緒に考える）。

## 補足

- この Skill 自体は汎用。特定の組織・社内リポジトリに依存しない。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] CLAUDE.md にプレースホルダ（`{{ }}`）が残っていない
- [ ] `.claude/rules/` に 4 ルール（commit-conventions/license-policy/no-secrets/branching）を配置した
- [ ] `block-main-push.sh` を `.claude/hooks/` に配置し **chmod +x** し、settings.json に PreToolUse を配線した
- [ ] `git init` + 初期コミット済み、デフォルトブランチが `main`
- [ ] `.env.example` に実値が入っていない / LICENSE 方針を確認した
