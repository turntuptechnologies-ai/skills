# skills

Turnt Up Technologies株式会社の [Claude Code](https://claude.com/claude-code) **Skill** 集。`turntup` プラグインとして install すると、Issue 起票 → 実装 → 品質ゲート → PR → リリースまでの開発フローを Skill として呼び出せる。

[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-d97757)](https://claude.com/claude-code)
[![Skills](https://img.shields.io/github/directory-file-count/turntuptechnologies-ai/skills/skills?type=dir&label=skills)](#スキル一覧--catalog)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

各 Skill は特定の組織・環境に依存する情報を含めず、どのプロジェクトでも汎用に動くように書いている（→ [運用ルール](#運用ルール)）。

## Skill とは

特定の作業のやり方を Claude に教える「手順書フォルダ」。実体は `SKILL.md`（Markdown + フロントマター）1 ファイル。

```
skills/<skill-name>/
  └── SKILL.md      ← 本体
  └── (任意) 補助スクリプト・参考資料
```

## インストール

前提: [Claude Code](https://claude.com/claude-code) がインストール済みであること。Claude Code 内で以下を実行する。

```bash
# マーケットプレイスを登録（一度だけ）
/plugin marketplace add turntuptechnologies-ai/skills

# プラグインを install
/plugin install turntup@turntup-skills

# 更新（リポジトリに変更が入ったら）
/plugin marketplace update turntup-skills
```

install 後、スキルは**名前空間付き**で呼び出す（組み込み・他プラグインの Skill と衝突しない）:

```
/turntup:create-pr
/turntup:pre-pr-checks
```

明示的に呼び出さなくても、Claude が各 Skill の `description` を見て自動的に使うかどうかを判断する。

## スキル一覧 / Catalog

install 後は `/turntup:<skill>` で呼び出す（Claude が `description` を見て自動で使うこともある）。

| 分類 | Skill | 用途 |
|---|---|---|
| 進行 | `run-agent-team` | Issue を Agent Teams で進める（architect→reviewer→developer→tester→documenter）。TeamCreate 不可時は Subagents で代替 |
| 進行 | `handoff` | セッションの作業状態を引き継ぎ書に保存・復元（新しいセッション開始・`/clear`・`/compact` 後は同梱 hook が自動注入） |
| 進行 | `create-issue` | 背景/提案/受け入れ条件の定型で Issue を起票（Issue → PR フローの入口） |
| 進行 | `debug-root-cause` | 再現→切り分け→根本原因→回帰テストの順でバグを修正（対症療法で終わらせない） |
| 立ち上げ | `new-project-init` | 共通規約で新規プロジェクト立ち上げ（CLAUDE.md / Rules / main 保護フック） |
| 立ち上げ | `repo-publish-security` | リポジトリ公開時のセキュリティ設定を点検・適用（secret scanning / 保護 ruleset / Actions 権限、公開前の履歴秘密情報チェック） |
| scaffold | `scaffold-wxt-extension` | WXT + React + Tailwind のブラウザ拡張 |
| scaffold | `scaffold-react-app` | Vite + React + Tailwind の SPA |
| scaffold | `scaffold-python-tool` | uv + ruff + mypy + pytest の Python ツール |
| scaffold | `scaffold-cf-worker` | Cloudflare Workers（wrangler + Hono） |
| scaffold | `scaffold-deno-api` | Deno + Hono + Drizzle の API サーバー |
| 品質ゲート | `pre-pr-checks` | stack 判定で format/lint/typecheck/test を一括実行 |
| 品質ゲート | `doc-sync` | ドキュメントの実装乖離を点検・修正 |
| 品質ゲート | `skill-lint` | SKILL.md をチェックリストで点検し、指摘は反証（敵対的検証）を経て確定（Skill 追加 PR の前に） |
| 品質ゲート | `adversarial-verify` | レビュー指摘の候補に反証を試み、生き残った指摘だけを確定（`skill-lint` / reviewer の検証フェーズ） |
| 提出 | `create-pr` | Conventional Commits タイトルで PR 作成 |
| 提出 | `pr-babysit` | PR の CI を監視し、失敗を修正して green になるまで面倒を見る |
| ドキュメント | `write-readme` | README を実証済み構成で整備 |
| 保守 | `dependency-update` | changelog・breaking 確認つきで依存を安全に更新（選定は `library-eval`） |
| 保守 | `release` | semver 判定・CHANGELOG・タグ・GitHub Release を一貫実行 |
| 調査 | `literature-review` | 論文・先行研究を引用付きでレビュー（arXiv/Semantic Scholar 等） |
| 調査 | `market-research` | 市場規模・競合・トレンドを出典付きで構造化 |
| 調査 | `library-eval` | 候補ライブラリを保守・採用・ライセンス・脆弱性で比較 |

## リポジトリ構成 / Layout

```
skills/           各 Skill（1 Skill = 1 ディレクトリ、SKILL.md 必須）
hooks/            プラグイン同梱 hook（hooks.json + スクリプト）
templates/        新規 Skill の雛形（SKILL.md）
scripts/          Skill 構造の機械検査（lint-skills.py。CI と手元で実行）
.github/          CI（workflows/ci.yml が scripts/lint-skills.py を実行）
.claude-plugin/   プラグイン定義（plugin.json / marketplace.json）
```

## 新しい Skill を追加する

1. `skills/<skill-name>/SKILL.md` を作る（雛形は [`templates/SKILL.md`](templates/SKILL.md)）
2. ローカルで試して `description` と手順を調整
3. `/turntup:skill-lint` で点検し、ブランチを切って PR（→ [運用ルール](#運用ルール)）。PR では CI が `scripts/lint-skills.py` で構造の機械検査を行う

## 運用ルール

- **固有情報を書かない** — 組織名・内部 URL・認証情報・固有プロジェクト名を Skill 本文に埋め込まない。環境差は環境変数や引数で渡し、どの環境でも汎用に動く状態を保つ。
- **1 Skill = 1 ディレクトリ**、`SKILL.md` 必須。
- **`description` が命** — 「いつ使うか・何をするか」を具体的に書く。これで発動可否が決まる。
- main 直 push 禁止。Issue → ブランチ → PR → merge。

## Skill と他の操縦手段

Skill は Claude Code を操縦する手段の一つで、「**呼び出して使う手順（procedure）**」に向く。常時効かせたい制約や確実に止めたいガードは、別の手段に分けるのが筋（下記記事の整理）。

| 手段 | 役割 | 置き場 |
|---|---|---|
| **Skill** | 呼び出して使う手順 | `.claude/skills/` |
| **CLAUDE.md** | プロジェクト概要・構成・規約 | リポジトリ各所 |
| **Rules** | 常に守る制約（パスでスコープ可） | `.claude/rules/` |
| **Hook** | モデルの判断を介さない確実な自動化・ブロック | `.claude/settings.json` |
| **Subagent** | 別コンテキストで実行し結果だけ返す | `.claude/agents/` |

`new-project-init` Skill は、新規プロジェクトに CLAUDE.md・Rules・main 保護フックのテンプレをまとめて撒く。

### プラグイン同梱 Hook

このプラグインは Skill に加えて hook（`hooks/hooks.json`）を同梱する。**plugin の hook は install した人の全プロジェクトで有効になる**点に注意。

| Hook | 発動 | やること |
|---|---|---|
| `load-handoff.sh` | SessionStart（`startup` / `clear` / `compact`。`resume` は対象外） | プロジェクトに `.claude/handoff/latest.md` があればコンテキストに自動注入（無ければ何もしない） |
| `compact-preserve.sh` | PreCompact | 要約に残すべき項目（ゴール・進捗・重要ファイル・決定事項・次の一手）のガイダンスを注入 |

> 表の `.claude/skills/` は standalone 配置の一般的な場所。**このリポジトリ自体は `turntup` プラグインとして配布**し、各 Skill は `skills/` 配下に置く。利用側は install 後 `/turntup:<skill>` で呼び出す（→ [インストール](#インストール)）。

## 参考 / References

- [Steering Claude Code: skills, hooks, rules, subagents, and more](https://claude.com/ja/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) — 各操縦手段の役割とロード方式・使い分け。本リポジトリの設計方針の土台。

## ライセンス / License

[MIT](LICENSE)
