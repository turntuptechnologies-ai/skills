---
name: pre-pr-checks
description: PR や push の前、コミットの前、または「チェックして」「lint かけて」「テスト通して」等と言われたとき。プロジェクトの stack を自動判定し、format / lint / typecheck / test を正しいコマンドで一括実行して結果を報告する。create-pr の前段として使う。
---

# 品質ゲート（PR 前チェック）

変更を提出する前に、そのリポジトリの標準チェックを一通り走らせて壊れていないか確認する。

## 手順

1. **リポジトリのルートで実行する。** マーカーファイルで stack を判定する（複数該当時は両方）。
2. **宣言済みの依存が未インストールなら、先にインストールする。** lockfile に従うプロジェクト自身のパッケージマネージャで入れる（`<pm> install` / `uv sync` 等）。プロジェクトが宣言済みの依存を入れるだけなので、ツールの新規導入には当たらない。ユーザーがインストールを止めている場合は実行せず、その旨を報告する。
3. 下表のコマンドを **format(check) → lint → typecheck → test** の順で実行する。
4. **設定ファイルに定義済みのコマンド（package.json の scripts 等）を最優先する。** 下表は無い場合のフォールバック。ただし中身が書き込み型（`--write` / `--fix` 等）の script はチェックに使わず、非破壊の同等コマンドで実行する（`format:check` 等の非破壊 script があればそれ、無ければ `biome format .` / `biome check .` のように書き込みフラグを外したもの）。チェック工程でファイルを書き換えると、検証対象の差分が変わってしまうため。
5. check ごとに pass / fail を報告する。fail があれば該当出力を示す。ツールがプロジェクトに未設定なら**スキップした旨を明記**する（勝手に導入しない）。設定されているのに起動できなかったチェック（コマンド未検出・依存不足・環境エラー）はスキップではなく **fail** とし、原因を備考に書く。

## stack 別コマンド

| マーカー | stack | format | lint | typecheck | test |
|---|---|---|---|---|---|
| `pyproject.toml` (+`uv.lock`) | Python (uv) | `uv run ruff format --check .` | `uv run ruff check .` | `uv run mypy src/` | `uv run pytest` |
| `package.json` | Node/TS | `<pm> run format:check` or `biome format .` | `<pm> run lint` | `<pm> run typecheck` / `tsc --noEmit` | `<pm> test` |
| `deno.json(c)` | Deno | `deno fmt --check` | `deno lint` | `deno check .` | `deno test` |
| `Cargo.toml` | Rust | `cargo fmt --check` | `cargo clippy -- -D warnings` | （clippy に含む） | `cargo test` |

### パッケージマネージャ判定（Node/TS）
- `pnpm-lock.yaml` → `pnpm` / `package-lock.json` → `npm` / `yarn.lock` → `yarn` / `bun.lockb` → `bun`
- まず `package.json` の `scripts` を見て、定義されている script 名（`lint` / `typecheck` / `check` / `test` / `format`）を使う。書き込み型の script は手順 4 のとおり非破壊の同等コマンドに置き換える。
- `biome.json` があれば lint/format は `biome` に寄せる。

## 結果の報告フォーマット

必ずこの表の形で報告する（結果は ✅ pass / ❌ fail / ⏭️ skip の3値）:

```markdown
| check | コマンド | 結果 | 備考 |
|---|---|---|---|
| format | `uv run ruff format --check .` | ✅ pass | |
| lint | `uv run ruff check .` | ❌ fail | E501 ×2（下に出力） |
| typecheck | `uv run mypy src/` | ✅ pass | |
| test | `uv run pytest` | ⏭️ skip | tests/ が存在しない |
```

fail がある場合は表の下に該当エラー出力を貼る。全て pass なら「`create-pr` で PR 作成に進めます」と添える。

## ルール・コツ

- **設定ファイル＞推測。** リポジトリが定めたコマンドがあれば必ずそれを使う。CI 設定（`.github/workflows`）に実行コマンドが書かれていれば、それを正とする。判定に迷ったら（scripts と CI で異なる等）推測で選ばずユーザーに確認する。
- format は基本 `--check`（破壊しない）。ユーザーが「直して」と言ったら format/lint の自動修正（`ruff check --fix`、`deno fmt`、`cargo fmt`、`<pm> run lint --fix`）を実行し、再チェックする。
- モノレポ/ワークスペースでは、変更があったパッケージ単位で実行する。
- 環境準備が必要な場合の例: Node 系は事前に `eval "$(mise activate bash)"` が要ることがある。失敗したらまず環境を確認する。
- すべて pass したら、続けて `create-pr` で PR を作成できる旨を伝える。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] リポジトリの全マーカーファイルを確認し、検出した stack を報告した
- [ ] 各チェック（format/lint/typecheck/test）を **実行 / 失敗 / スキップ** のいずれかで漏れなく報告した（スキップには理由を付す）
- [ ] fail があれば該当する出力（エラーメッセージ）を提示した
- [ ] 設定ファイル（scripts / CI）に定義済みコマンドがあるか確認してから、フォールバック表を使った
- [ ] チェック工程でファイルを書き換えていない（書き込み型の script を非破壊の同等コマンドに置き換えた）
- [ ] 起動できなかったチェックをスキップではなく fail とし、原因を報告した
- [ ] ツールの新規導入・設定変更をしていない（宣言済み依存のインストールは除く）

## 補足

- 社名・内部 URL・認証情報などの固有情報は扱わない。
