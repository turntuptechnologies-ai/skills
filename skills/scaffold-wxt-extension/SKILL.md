---
name: scaffold-wxt-extension
description: ブラウザ拡張機能を新規に作るとき。「拡張機能を作る」「WXT で拡張を立ち上げ」等で使う。WXT + React + TypeScript + Tailwind CSS v4 + Vitest の構成で雛形を用意する。土台（CLAUDE.md・git）は new-project-init を先に使う。
---

# ブラウザ拡張 scaffold（WXT + React + TS + Tailwind）

[WXT](https://wxt.dev) ベースで、Chrome / Firefox 両対応の拡張を雛形生成する。

## stack

- パッケージマネージャ: **pnpm**
- フレームワーク: **WXT** + **React 19**（`@wxt-dev/module-react`）
- スタイル: **Tailwind CSS v4**（`@tailwindcss/vite`）
- テスト: **Vitest**（`jsdom`）
- 型チェック: `tsc --noEmit`
- アイコン: `@wxt-dev/auto-icons`（任意）

## 手順

1. **初期化** — 空ディレクトリで WXT を初期化し、React テンプレートを選ぶ。
   ```bash
   pnpm dlx wxt@latest init .
   # テンプレートで react / TypeScript を選択
   pnpm install
   ```
2. **Tailwind v4 を追加**
   ```bash
   pnpm add tailwindcss @tailwindcss/vite
   ```
   `wxt.config.ts` の vite plugins に `tailwindcss()` を足し、エントリ CSS に `@import "tailwindcss";` を書く。
3. **Vitest を追加**
   ```bash
   pnpm add -D vitest jsdom
   ```
4. **package.json の scripts を揃える**
   ```jsonc
   {
     "dev": "wxt",
     "dev:firefox": "wxt -b firefox",
     "build": "wxt build",
     "build:firefox": "wxt build -b firefox",
     "zip": "wxt zip",
     "compile": "tsc --noEmit",
     "test": "vitest run",
     "postinstall": "wxt prepare"
   }
   ```
5. **`wxt.config.ts` の骨子**
   ```ts
   import { defineConfig } from 'wxt';
   import tailwindcss from '@tailwindcss/vite';

   export default defineConfig({
     modules: ['@wxt-dev/module-react'],
     vite: () => ({ plugins: [tailwindcss()] }),
     manifest: {
       name: '{{ 拡張名 }}',
       description: '{{ 説明 }}',
       permissions: [/* 例: 'activeTab', 'storage' */],
       host_permissions: [/* 必要な対象オリジンのみ。広すぎる権限を避ける */],
     },
   });
   ```
6. **動作確認** — `pnpm dev`（Chrome）/ `pnpm dev:firefox`。型・テストは `pre-pr-checks` で確認。

## ルール・コツ

- **権限は最小限に。** `permissions` / `host_permissions` は必要なものだけ。`<all_urls>` は避ける。
- エントリポイントは `entrypoints/`（`popup`, `content`, `background` 等）。UI は React コンポーネントで作る。
- `postinstall: wxt prepare` を入れると型生成が走り、初回 clone 後の型エラーを防げる。
- Firefox 配布も視野なら `build:firefox` / `zip:firefox` も用意する。

## 補足

- 機密値（API キー等）はコードに埋め込まない。設定 UI かビルド時の環境変数で扱う。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] `pnpm install` が通り、`pnpm dev` で拡張が起動する
- [ ] scripts（dev/build/zip/compile/test/postinstall）が揃っている
- [ ] Tailwind v4 が vite plugin + エントリ CSS で有効になっている
- [ ] manifest の permissions / host_permissions が必要最小限（`<all_urls>` を使っていない）
- [ ] 機密値をコードに埋め込んでいない
