# skills

社内で共有して使う [Claude Code](https://claude.com/claude-code) の **Skill** 置き場。

将来的に社外 OSS 公開も視野に入れているため、各 Skill は **社内固有情報を一切含めず、汎用的に動く**ように書く（→ [運用ルール](#運用ルール)）。

## Skill とは

特定の作業のやり方を Claude に教える「手順書フォルダ」。実体は `SKILL.md`（Markdown + フロントマター）1 ファイル。

```
skills/<skill-name>/
  └── SKILL.md      ← 本体
  └── (任意) 補助スクリプト・参考資料
```

## 使い方（各メンバー）

このリポジトリは Claude Code の**プラグイン**（`turntup`）として配布する。**private リポのまま**、各自の GitHub 権限で install できる（公開はされない）。

```bash
# マーケットプレイスを登録（一度だけ。アクセスは gh の権限で gate される）
/plugin marketplace add turntuptechnologies-ai/skills

# プラグインを install
/plugin install turntup@turntup-skills

# 更新（リポに変更が入ったら）
/plugin marketplace update turntup-skills
```

install 後、スキルは**名前空間付き**で呼び出す（他スキルと衝突しない）:

```
/turntup:create-pr
/turntup:pre-pr-checks
```

`description` を見て Claude が自動的に使うかどうかも判断する。

> プラグイン化により名前空間（`turntup:`）が付くため、generic なスキル名でも組み込み/他プラグインと衝突しない。`plugin.json` / `marketplace.json` を足してもリポジトリは private のまま。Anthropic のコミュニティ marketplace への**明示的な申請をしない限り公開されない**。

## スキル一覧 / Catalog

install 後は `/turntup:<skill>` で呼び出す（Claude が `description` を見て自動で使うこともある）。

| 分類 | Skill | 用途 |
|---|---|---|
| 進行 | `run-agent-team` | Issue を Agent Teams で進める（architect→reviewer→developer→tester→documenter） |
| 立ち上げ | `new-project-init` | 共通規約で新規プロジェクト立ち上げ（CLAUDE.md / Rules / main 保護フック） |
| scaffold | `scaffold-wxt-extension` | WXT + React + Tailwind のブラウザ拡張 |
| scaffold | `scaffold-react-app` | Vite + React + Tailwind の SPA |
| scaffold | `scaffold-python-tool` | uv + ruff + mypy + pytest の Python ツール |
| scaffold | `scaffold-cf-worker` | Cloudflare Workers（wrangler + Hono） |
| scaffold | `scaffold-deno-api` | Deno + Hono + Drizzle の API サーバー |
| 品質ゲート | `pre-pr-checks` | stack 判定で format/lint/typecheck/test を一括実行 |
| 品質ゲート | `doc-sync` | ドキュメントの実装乖離を点検・修正 |
| 提出 | `create-pr` | Conventional Commits タイトルで PR 作成 |
| ドキュメント | `write-readme` | README を実証済み構成で整備 |
| 調査 | `literature-review` | 論文・先行研究を引用付きでレビュー（arXiv/Semantic Scholar 等） |
| 調査 | `market-research` | 市場規模・競合・トレンドを出典付きで構造化 |
| 調査 | `library-eval` | 候補ライブラリを保守・採用・ライセンス・脆弱性で比較 |

## 新しい Skill を追加する

1. `skills/<skill-name>/SKILL.md` を作る（雛形は [`templates/SKILL.md`](templates/SKILL.md)）
2. ローカルで試して `description` と手順を調整
3. ブランチを切って PR（→ [運用ルール](#運用ルール)）

## 運用ルール

- **社内固有情報を書かない** — 社名・組織名・内部 URL・認証情報・固有プロジェクト名を Skill 本文に埋め込まない。環境差は環境変数や引数で渡す。公開時に履歴を漁られても問題ない状態を最初から保つ。
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

> 表の `.claude/skills/` は standalone 配置の一般的な場所。**このリポジトリ自体は `turntup` プラグインとして配布**し、各 Skill は `skills/` 配下に置く。利用側は install 後 `/turntup:<skill>` で呼び出す（→ [使い方](#使い方各メンバー)）。

## 参考 / References

- [Steering Claude Code: skills, hooks, rules, subagents, and more](https://claude.com/ja/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) — 各操縦手段の役割とロード方式・使い分け。本リポジトリの設計方針の土台。
