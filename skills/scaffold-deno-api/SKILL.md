---
name: scaffold-deno-api
description: Deno で型付きの API サーバー（REST/JSON）を新規に作るとき。「Deno で API を作る」「Hono+Drizzle でバックエンドを立ち上げ」等で使う。Deno + Hono + Drizzle ORM + PostgreSQL の構成で雛形を用意する。土台は new-project-init を先に使う。
---

# Deno API サーバー scaffold（Deno + Hono + Drizzle + PostgreSQL）

Deno ランタイム上に、型付きの REST/JSON API サーバーを雛形生成する。

## stack

- ランタイム: **Deno**（依存は `deno.json` の `imports`、npm/jsr を直接参照）
- ルーティング: **Hono**（OpenAPI を出すなら `@hono/zod-openapi` + `@hono/swagger-ui`）
- ORM: **Drizzle ORM** + **drizzle-kit**、ドライバ **postgres-js**、DB **PostgreSQL**
- バリデーション: **Zod**
- テスト: `deno test`（標準 `@std/assert` / `@std/testing`）
- lint/format: `deno lint` / `deno fmt`、型: `deno check`

## 手順

1. **初期化** — 空ディレクトリで `deno init` するか手で `deno.json` を作る。
2. **`deno.json` の `imports` を定義**（npm/jsr を直接参照）
   ```jsonc
   {
     "imports": {
       "hono": "npm:hono@^4",
       "@hono/zod-openapi": "npm:@hono/zod-openapi@^0.18",
       "@hono/swagger-ui": "npm:@hono/swagger-ui@^0.5",
       "drizzle-orm": "npm:drizzle-orm@^0.38",
       "drizzle-orm/pg-core": "npm:drizzle-orm@^0.38/pg-core",
       "drizzle-orm/postgres-js": "npm:drizzle-orm@^0.38/postgres-js",
       "drizzle-kit": "npm:drizzle-kit@^0.30",
       "postgres": "npm:postgres@^3",
       "zod": "npm:zod@^3",
       "@std/assert": "jsr:@std/assert@^1",
       "@std/testing": "jsr:@std/testing@^1"
     },
     "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true },
     "lock": { "frozen": true },
     "nodeModulesDir": "auto",
     "exclude": ["node_modules/", "drizzle/"]
   }
   ```
3. **`deno.json` の `tasks` を揃える**（権限は最小限で明示）
   ```jsonc
   {
     "tasks": {
       "dev": "deno run --watch --env --allow-env --allow-net --allow-read src/main.ts",
       "start": "deno run --env --allow-env --allow-net --allow-read src/main.ts",
       "test": "deno test --env --allow-env --allow-net --allow-read --ignore=src/**/*_integration_test.ts",
       "test:integration": "deno test --env --allow-env --allow-net --allow-read src/**/*_integration_test.ts",
       "lint": "deno lint",
       "fmt": "deno fmt",
       "fmt:check": "deno fmt --check",
       "check": "deno check --frozen src/**/*.ts",
       "db:generate": "deno run --env --allow-env --allow-sys=homedir --allow-run --allow-net --allow-read --allow-write --node-modules-dir npm:drizzle-kit generate",
       "db:migrate": "deno run --env --allow-env --allow-sys=homedir --allow-run --allow-net --allow-read --allow-write --node-modules-dir npm:drizzle-kit migrate",
       "db:studio": "deno run --env --allow-env --allow-sys=homedir --allow-run --allow-net --allow-read --node-modules-dir npm:drizzle-kit studio"
     }
   }
   ```
4. **`drizzle.config.ts`**
   ```ts
   import { defineConfig } from "drizzle-kit";
   const url = Deno.env.get("DATABASE_URL");
   if (!url) throw new Error("DATABASE_URL が設定されていません");
   export default defineConfig({
     out: "./drizzle",
     schema: "./src/db/schema/index.ts",
     dialect: "postgresql",
     dbCredentials: { url },
   });
   ```
5. **ディレクトリ構成**（目安）
   ```
   src/
     main.ts            # エントリ（サーバ起動）
     app.ts             # Hono アプリ組み立て
     routes/            # ルートハンドラ
     services/          # ビジネスロジック
     db/
       schema/index.ts  # Drizzle スキーマ
       client.ts        # postgres-js 接続
     middleware/        # 認証・エラー処理等
     validators/        # Zod スキーマ
   ```
6. **PostgreSQL を起動**（Docker） → `deno task db:generate` → `db:migrate`。
7. **動作確認** — `deno task dev`。lint/fmt/check/test は `pre-pr-checks`（Deno を検出して実行）。

## ルール・コツ

- **Deno の permissions は最小限を明示する**（`--allow-net --allow-env --allow-read` など）。広い権限を避ける。
- **`strict` + `noUncheckedIndexedAccess`** を有効に。型を最初から付ける。
- **テスト規約**: 単体は `*_test.ts`、DB/外部を含む統合は `*_integration_test.ts`。task で切り分ける。
- DB スキーマ変更は `db:generate`（マイグレーション生成）→ レビュー → `db:migrate`。`db:push` は開発時のみ。
- 機密（`DATABASE_URL` 等）は環境変数（`.env`＋`--env`）。コミットは `.env.example` のみ（→ no-secrets ルール）。
- OpenAPI ドキュメントが要るなら `@hono/zod-openapi` でスキーマ駆動にし、`@hono/swagger-ui` で配信する。

## 補足

- 命名は runtime（Deno）で識別。Cloudflare Workers なら `scaffold-cf-worker` を使う。
- ライセンスは permissive 前提。固有情報は埋め込まない。
- 記載のバージョン・パッケージ構成は Skill 作成時点の目安。初期化時に最新安定版を確認して読み替える。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] deno.json の tasks / imports が揃い、`deno task check` と `deno task lint` が通る
- [ ] compilerOptions が strict + noUncheckedIndexedAccess、lock frozen
- [ ] tasks の permissions が最小限で明示されている（広い権限を使っていない）
- [ ] drizzle.config.ts が DATABASE_URL（環境変数）を参照し、実値をコミットしていない
- [ ] テストが `_test.ts` / `_integration_test.ts` 規約で task 分離されている
