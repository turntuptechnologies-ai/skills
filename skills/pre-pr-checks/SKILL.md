---
name: pre-pr-checks
description: PR や push の前、コミットの前、または「チェックして」「lint かけて」「テスト通して」等と言われたとき。プロジェクトの stack を自動判定し、format / lint / typecheck / test を正しいコマンドで一括実行して結果を報告する。create-pr の前段として使う。
---

# 品質ゲート（PR 前チェック）

変更を提出する前に、そのリポジトリの標準チェックを一通り走らせて壊れていないか確認する。

## 手順

1. **リポジトリのルートで実行する。** マーカーファイルで stack を判定する（複数該当時は両方）。
2. 下表のコマンドを **format(check) → lint → typecheck → test** の順で実行する。
3. **設定ファイルに定義済みのコマンド（package.json の scripts 等）を最優先する。** 下表は無い場合のフォールバック。
4. check ごとに pass / fail を報告する。fail があれば該当出力を示す。ツールが未設定なら**スキップした旨を明記**する（勝手に導入しない）。

## stack 別コマンド

| マーカー | stack | format | lint | typecheck | test |
|---|---|---|---|---|---|
| `pyproject.toml` (+`uv.lock`) | Python (uv) | `uv run ruff format --check .` | `uv run ruff check .` | `uv run mypy src/` | `uv run pytest` |
| `package.json` | Node/TS | `<pm> run format` or `biome format .` | `<pm> run lint` | `<pm> run typecheck` / `tsc --noEmit` | `<pm> test` |
| `deno.json(c)` | Deno | `deno fmt --check` | `deno lint` | `deno check .` | `deno test` |
| `Cargo.toml` | Rust | `cargo fmt --check` | `cargo clippy -- -D warnings` | （clippy に含む） | `cargo test` |

### パッケージマネージャ判定（Node/TS）
- `pnpm-lock.yaml` → `pnpm` / `package-lock.json` → `npm` / `yarn.lock` → `yarn` / `bun.lockb` → `bun`
- まず `package.json` の `scripts` を見て、定義されている script 名（`lint` / `typecheck` / `check` / `test` / `format`）を使う。
- `biome.json` があれば lint/format は `biome` に寄せる。

## ルール・コツ

- **設定ファイル＞推測。** リポジトリが定めたコマンドがあれば必ずそれを使う。CI 設定（`.github/workflows`）に実行コマンドが書かれていれば、それを正とする。
- format は基本 `--check`（破壊しない）。ユーザーが「直して」と言ったら format/lint の自動修正（`ruff check --fix`、`deno fmt`、`cargo fmt`、`<pm> run lint --fix`）を実行し、再チェックする。
- モノレポ/ワークスペースでは、変更があったパッケージ単位で実行する。
- 環境準備が必要な場合の例: Node 系は事前に `eval "$(mise activate bash)"` が要ることがある。失敗したらまず環境を確認する。
- すべて pass したら、続けて `create-pr` で PR を作成できる旨を伝える。

## 補足

- 社名・内部 URL・認証情報などの固有情報は扱わない。
