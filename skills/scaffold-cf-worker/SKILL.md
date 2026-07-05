---
name: scaffold-cf-worker
description: Cloudflare Workers のサーバレスアプリ/API を新規に作るとき。「Workers でアプリを作る」「Cloudflare で API を立ち上げ」等で使う。wrangler + Hono + TypeScript + Vitest(workers pool) + Biome の構成で雛形を用意する。土台は new-project-init を先に使う。
---

# Cloudflare Workers scaffold（wrangler + Hono + TS）

Cloudflare Workers 上のアプリ/API を雛形生成する。

> **詳細とベストプラクティスは組み込み Skill に委ねる。** ルーティング設計やバインディングの作法、wrangler のサブコマンド、アンチパターン回避は `cloudflare` / `workers-best-practices` / `wrangler` Skill を併用する。本 Skill は「最初の雛形を組む手順」に集中する。

## stack

- パッケージマネージャ: **pnpm**、CLI: **wrangler 4**
- ルーティング: **Hono**
- 言語: **TypeScript**（`wrangler types` で型生成）
- テスト: **Vitest** + **`@cloudflare/vitest-pool-workers`**（Workers ランタイム上で実行）
- lint/format: **Biome**
- 設定: **`wrangler.jsonc`**

## 手順

1. **初期化**
   ```bash
   pnpm create cloudflare@latest <name> -- --framework=hono --lang=ts
   # または既存ディレクトリで wrangler を導入し、手で構成してもよい
   pnpm install
   ```
2. **lint/test を追加**
   ```bash
   pnpm add -D @biomejs/biome vitest @cloudflare/vitest-pool-workers
   ```
3. **`package.json` の scripts を揃える**
   ```jsonc
   {
     "dev": "wrangler dev",
     "deploy": "wrangler deploy",
     "test": "vitest run",
     "types": "wrangler types --strict-vars=false",
     "typecheck": "tsc --noEmit",
     "lint": "biome check .",
     "format": "biome format --write ."
   }
   ```
4. **`wrangler.jsonc` の骨子**
   ```jsonc
   {
     "$schema": "node_modules/wrangler/config-schema.json",
     "name": "<name>",
     "main": "src/index.ts",
     "compatibility_date": "{{ 最新の日付 }}",
     "compatibility_flags": ["nodejs_compat"],
     "observability": { "enabled": true }
     // バインディングは必要に応じて追加（下記）
   }
   ```
5. **バインディングを足す**（使うものだけ）
   - **D1**: `wrangler d1 create <db>` → `d1_databases` に `binding`/`database_name`/`database_id`/`migrations_dir` を追記。マイグレーションは `wrangler d1 migrations apply <db>`。
   - **R2**: `wrangler r2 bucket create <bucket>` → `r2_buckets` に `binding`/`bucket_name`。
   - **KV**: `wrangler kv namespace create <ns>` → `kv_namespaces`。
   - **Cron**: `triggers.crons` に式を追記し、`scheduled` ハンドラを実装。
   - 非機密の設定は `vars`、**機密は `wrangler secret put <KEY>`**（`vars` に置かない）。
6. **型生成 → 動作確認**
   ```bash
   pnpm types        # env バインディングの型を生成
   pnpm dev          # ローカル起動
   ```
   型・lint・テストは `pre-pr-checks`、デプロイは `wrangler deploy`。

## ルール・コツ

- **`compatibility_date` は新規作成時点の日付**にする。Node 互換が要るなら `nodejs_compat`。
- **observability を有効化**しておく（ログ・メトリクスの土台）。
- **秘密情報は `vars` に書かない。** `wrangler secret put` か Secrets Store を使う（→ no-secrets ルール）。`database_id` 等の置換が要る箇所はプレースホルダにし、実値はコミットしない。
- テストは `@cloudflare/vitest-pool-workers` で Workers ランタイム上の挙動を検証する。
- バインディングを足したら `pnpm types` を再実行して型を更新する。
- 詳細な設計判断・落とし穴は `workers-best-practices` Skill を必ず参照する。

## 補足

- ライセンスは permissive 前提。social/固有情報は埋め込まない。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] `pnpm install` が通り、`pnpm dev`（wrangler dev）で起動する
- [ ] scripts（dev/deploy/test/types/typecheck/lint/format）が揃っている
- [ ] wrangler.jsonc に compatibility_date（作成時点の日付）/ nodejs_compat / observability がある
- [ ] バインディング追加後に `pnpm types` を実行し型を更新した
- [ ] 機密を vars に書いていない（wrangler secret を案内）/ database_id 等の実値をコミットしていない
