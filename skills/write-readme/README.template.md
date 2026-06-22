<!-- README テンプレート。見出し・言語はリポジトリの慣習に合わせて訳す（public OSS は英語、社内向けは日本語など）。
     当てはまらないセクションは削除し、必要なら足す。各記載は実装から裏を取って書くこと。 -->

# {{ プロジェクト名 }}

{{ 1〜2 行で「何をするものか・何を解決するか」。バッジ（CI / license 等）があればこの下に。 }}

## 概要 / What it does

{{ もう少し具体的に、主要な機能や使いどころを箇条書きで。 }}

- {{ 機能 1 }}
- {{ 機能 2 }}

## 技術構成 / Stack

- {{ 言語・ランタイム（例: TypeScript / Node 22, Python 3.12） }}
- {{ 主要フレームワーク・ライブラリ }}
- {{ データストア・インフラ（あれば） }}

## クイックスタート / Quick start

```bash
{{ 取得 }}        # 例: git clone ... && cd ...
{{ 依存インストール }}  # 例: pnpm install / uv sync
{{ 起動 }}        # 例: pnpm dev / uv run <cmd>
```

{{ 前提条件（必要なランタイム・バージョン・外部サービス）があれば明記。 }}

## 設定 / Configuration

{{ 環境変数・設定ファイルの説明。実値は書かず .env.example を案内する。 }}

| 変数 / キー | 説明 | 既定値 |
|---|---|---|
| `{{ KEY }}` | {{ 説明 }} | {{ 既定値 }} |

## 構成 / Layout

{{ 初見で迷いやすいディレクトリの役割。全列挙は不要。 }}

```
src/        # {{ 説明 }}
docs/       # {{ 説明 }}
```

## ドキュメント / Documentation

- [{{ 例: アーキテクチャ }}](docs/ARCHITECTURE.md)
- [{{ 例: デプロイ }}](docs/DEPLOY.md)

## 開発 / Development

```bash
{{ lint }}        # 例: pnpm lint / uv run ruff check .
{{ test }}        # 例: pnpm test / uv run pytest
{{ build }}       # 例: pnpm build
```

{{ 開発フロー（Issue → ブランチ → PR）への簡単な言及。詳細は CONTRIBUTING / CLAUDE.md へ。 }}

## ライセンス / License

{{ 例: MIT — see [LICENSE](LICENSE) }}
