---
name: scaffold-react-app
description: React のフロントエンド/SPA Web アプリを新規に作るとき。「React アプリを作る」「Vite でフロントを立ち上げ」等で使う。Vite + React + TypeScript + Tailwind v4 + Vitest の構成で雛形を用意する（API 連携なら TanStack Query）。土台は new-project-init を先に使う。
---

# React Web アプリ scaffold（Vite + React + TS + Tailwind）

Vite ベースの React 19 + TypeScript SPA を雛形生成する。

## stack

- パッケージマネージャ: **pnpm**（Node 22+）
- ビルド: **Vite** + `@vitejs/plugin-react`
- UI: **React 19** + **react-router-dom**
- スタイル: **Tailwind CSS v4**（`@tailwindcss/vite`）
- テスト: **Vitest** + **@testing-library/react** + `jsdom`
- lint/format: **Biome**（既定）/ 型: `tsc -b`
- 任意: **TanStack Query**（API データ取得）, **Recharts**（グラフ）, SSE は `EventSource`

## 手順

1. **初期化**
   ```bash
   pnpm create vite@latest . --template react-ts
   pnpm install
   ```
2. **Tailwind v4 を追加**
   ```bash
   pnpm add tailwindcss @tailwindcss/vite
   ```
   `vite.config.ts` の plugins に `tailwindcss()` を足し、エントリ CSS に `@import "tailwindcss";`。
3. **ルーティング / データ取得（必要に応じて）**
   ```bash
   pnpm add react-router-dom
   pnpm add @tanstack/react-query     # API 連携するなら
   ```
4. **テストと lint を追加**
   ```bash
   pnpm add -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event @vitest/coverage-v8
   pnpm add -D @biomejs/biome
   ```
5. **package.json の scripts を揃える**
   ```jsonc
   {
     "dev": "vite",
     "build": "tsc -b && vite build",
     "preview": "vite preview",
     "test": "vitest",
     "test:run": "vitest run",
     "lint": "biome lint",
     "format": "biome format --write",
     "check": "biome check --write"
   }
   ```
6. **`vite.config.ts` の骨子**
   ```ts
   import { defineConfig } from 'vite';
   import react from '@vitejs/plugin-react';
   import tailwindcss from '@tailwindcss/vite';

   export default defineConfig({
     plugins: [react(), tailwindcss()],
     test: { environment: 'jsdom', setupFiles: ['./src/test/setup.ts'] },
   });
   ```
7. **動作確認** — `pnpm dev`。型・lint・テストは `pre-pr-checks` で確認。

## ルール・コツ

- **API 連携は TanStack Query** に寄せる（キャッシュ・再取得・ローディング状態を一元管理）。リアルタイム更新は `EventSource`(SSE)。
- ルーティングは `react-router-dom`。型安全なローダ/アクションを活用する。
- テストは Testing Library で**ユーザー視点**（role/label で取得、実装詳細に依存しない）。
- 環境変数は Vite の `import.meta.env.VITE_*`。秘密情報をフロントに埋め込まない（公開される）。
- グラフが必要なら Recharts。

## 補足

- ライセンスは permissive 前提。依存追加時にライセンスを確認する。
