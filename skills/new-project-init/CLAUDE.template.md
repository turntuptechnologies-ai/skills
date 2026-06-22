# {{ プロジェクト名 }}

{{ 何を作るのか・何を解決するのかを簡潔に。 }}

## プロジェクトフェーズ

現在: **{{ 現在のフェーズ }}**

| フェーズ | 意味 | 状態 |
|---|---|---|
| **PROTOTYPE** | 試作期 | 試作・検証中。コア機能の開発とプロトタイピング |
| **ALPHA / BETA** | 検証期 | 主要機能が揃い、フィードバック収集・改善中 |
| **PREVIEW** | 公開準備期 | 本番環境に近い状態で最終調整 |
| **STABLE** | 安定稼働期 | 正式リリース。安定稼働中 |

## 言語・ツール

- 言語: {{ 例: TypeScript, Python, Rust }}
- フレームワーク: {{ 例: React, FastAPI, axum }}
- DB: {{ 例: PostgreSQL, SQLite（不要なら削除） }}
- ビルド: `{{ コマンド }}`
- テスト: `{{ コマンド }}`
- リント: `{{ コマンド }}`
- フォーマット: `{{ コマンド }}`

## ディレクトリ構成

{{ 初見で迷いやすい構成・重要なディレクトリの役割を説明する。全列挙は不要。 }}

## コーディング規約

- フォーマッタ / リンタ: {{ 例: ruff, biome, cargo fmt+clippy }}
- 命名規則: {{ 型=PascalCase / 関数・変数=camelCase or snake_case / 定数=SCREAMING_SNAKE_CASE / ファイル=kebab-case }}

## テスト戦略

{{ テストの種類・配置・実行方法を記述する。 }}

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/) に従う（`<type>: <description> (#<issue-number>)`）。
詳細は常時効く制約として `.claude/rules/commit-conventions.md` を正とする。description は {{ 言語 }} で記述する。

## 開発フロー

1. **Issue 作成** — コード/ドキュメント変更には必ず Issue を作る。判断の経緯を Issue に記録する。
2. **ブランチ作成** — `issue-<番号>/<簡単な説明>`（例: `issue-42/add-user-auth`）。
3. **実装** — 作業中は適宜 commit・push。**main への直接 push は禁止**（`.claude/rules/branching.md` ＋ `block-main-push.sh` フックで担保）。
4. **PR 作成** — Issue を参照（`Closes #42`）。
5. **コードレビュー** — マージ前にレビュー（セキュリティ観点を含む）。
6. **squash merge → ブランチ削除**。

## ライセンスルール

permissive ライセンス（MIT / Apache-2.0 / BSD / ISC 等）のみを使い、GPL 系の依存は避ける。
詳細は常時効く制約として `.claude/rules/license-policy.md` を正とする。

## 環境ルール

- sudo は使用しない。ランタイム/ツールのインストールには mise を使う。
- サービスやミドルウェアが必要なら Docker（`docker-compose.yaml`）で管理する。

## 言語ルール

- Issue・PR・コミット等の自然言語はすべて {{ 言語 }} で記述する。

<!-- Agent Teams を使う場合は、claude-md-templates の agent-teams セクションをここに追記する。 -->
