---
name: release
description: リリース作業をするとき。「リリースして」「バージョン上げて」「タグ切って」「CHANGELOG 更新して」等で使う。前回タグからの変更を集めて Conventional Commits から semver でバージョンを決め、バージョンファイル更新・CHANGELOG・タグ・GitHub Release までを一貫して行う。
---

# リリース（release）

## このスキルがやること

前回リリースからの変更を棚卸しし、バージョン決定 → バージョンファイル更新 → CHANGELOG → タグ → GitHub Release を漏れなく一貫して行う。

## 手順

1. **前回リリースを特定する**: `git describe --tags --abbrev=0`。タグが無ければ初回リリースとして扱い、初期バージョン（`v0.1.0` か `v1.0.0` か）をユーザーに確認する。
2. **変更を収集する**: `git log <last-tag>..HEAD --oneline`。リリース対象の変更が無ければその旨を報告して終了する。
3. **バージョンを判定する**（Conventional Commits から機械的に）:

   | 前回タグ以降のコミット | bump |
   |---|---|
   | `BREAKING CHANGE` / `<type>!:` を含む | major |
   | `feat:` を含む（BREAKING なし） | minor |
   | `fix:` / その他のみ | patch |

   - `0.x` 系は breaking でも minor に留める慣習があるため、major 相当の変更がある場合はどちらにするかユーザーに確認する。
4. **バージョンファイルを更新する**: リポジトリ内の全バージョン記載箇所（`package.json` / `pyproject.toml` / `Cargo.toml` / `deno.json` / `.claude-plugin/plugin.json` 等、存在するもの）を grep で洗い出し、**全て新バージョンで一致**させる。
5. **CHANGELOG.md を更新する**（無ければ [Keep a Changelog](https://keepachangelog.com/) 形式で新規作成）: `## [X.Y.Z] - YYYY-MM-DD` の節に Added / Changed / Fixed で振り分け、PR/Issue 番号を添える。
6. **リリースする**:
   - リリースコミット `chore: release vX.Y.Z` を作る。main が保護されていれば PR 経由でマージする（create-pr）
   - マージ後の main のコミットにタグ `vX.Y.Z` を打って push する（`git tag vX.Y.Z && git push origin vX.Y.Z`）
   - `gh release create vX.Y.Z --title "vX.Y.Z" --notes "<CHANGELOG の該当節>"` で GitHub Release を作成する
7. **URL を報告する**。

## ルール・コツ

- **タグは必ず merge 後の main のコミットに打つ**（PR ブランチのコミットに打たない）。
- バージョンファイルとタグに既に不一致がある場合（タグだけ進んでいる等）は、勝手に整合させず現状を報告して方針を確認する。
- CHANGELOG には「利用者に見える変化」を書く。内部リファクタは Changed に 1 行で足りる。コミットログの丸写しをしない。
- CI にリリースワークフロー（tag push トリガーで publish 等）がある場合はそれに従い、手動 publish と二重にしない。ワークフローの有無を `.github/workflows` で確認する。
- リリース直前に main の CI が green であることを確認する（落ちていたら pr-babysit / 修正が先）。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] バージョン判定の根拠（該当コミットと適用した semver 規則）を報告した
- [ ] リポジトリ内の全バージョン記載箇所を洗い出し、新バージョンで一致していることを確認した
- [ ] CHANGELOG に今回リリース分の節（日付・Added/Changed/Fixed）がある
- [ ] タグが main のリリースコミットに打たれ、push されている
- [ ] GitHub Release を作成し URL を報告した（作成できない場合は理由を報告）

## 補足

- 社名・内部 URL・認証情報などの固有情報は扱わない。
- パッケージレジストリへの publish（npm publish 等）はこのスキルの範囲外。必要ならユーザーに確認してから行う。
