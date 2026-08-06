---
name: write-readme
description: README を新規に作る、または既存の README を実証済みの構成で整え直すとき。「README を書いて/整えて」「README が薄い・構成を揃えたい」等で使う。概要/Stack/Quick start/Configuration/Layout/Documentation/Development/License の構成で、実装から裏を取って書く。
---

# README 整備（write-readme）

プロジェクトの README を、チームで実証済みの構成で作成・標準化する。リポ間のバラつきを解消し、公開しても通用する品質にする。

## 構成（標準セクション）

同梱の [`README.template.md`](README.template.md) をベースにする。順序と意図は以下。

1. **タイトル + 一文要約** — 何をするものか。バッジ（CI/license）があれば直下。
2. **概要 / What it does** — 主要機能・使いどころを箇条書き。
3. **技術構成 / Stack** — 言語・フレームワーク・データストア。
4. **クイックスタート / Quick start** — clone → install → 起動 を**コピペで動く**コマンドで。前提条件も。
5. **設定 / Configuration** — 環境変数・設定キー（実値は書かず `.env.example` を案内）。
6. **構成 / Layout** — 迷いやすいディレクトリの役割。
7. **ドキュメント / Documentation** — `docs/` 配下への索引。
8. **開発 / Development** — lint/test/build コマンド、開発フローへの言及。
9. **ライセンス / License**。

## 手順

1. **事実を集める** — `package.json`/`pyproject.toml` 等の scripts・依存、`.env.example`、ディレクトリ構成、CLI/エントリポイントを読み、記載の根拠を実装から取る。
2. **テンプレを埋める** — `README.template.md` をコピーし、当てはまらないセクションは削除、必要なら足す。
3. **コマンドを検証する** — Quick start / Development のコマンドが実際に通るか確認する（少なくとも scripts に存在するか裏取り）。
4. **既存 README がある場合** — 構成をこのテンプレに寄せつつ、既にある正確な記述は活かす。全消し再生成はしない。

## ルール・コツ

- **言語・見出しはリポジトリの慣習に合わせる。** public OSS は英語、社内向けは日本語、など。テンプレの `概要 / What it does` 形式の併記は適宜どちらかに寄せる。
- **推測で書かない。** 動かないコマンド・存在しないオプションを書かない。確認できないものは実行/参照して裏を取る。
- **コピペで動く**ことを最優先（特に Quick start）。前提（ランタイム/バージョン/外部サービス）を省かない。
- 秘密情報・固有情報を書かない（→ no-secrets ルール）。設定値は `.env.example` を案内。
- 新規プロジェクトの初期 README は `new-project-init` が用意する。本 Skill はそれを充実させる/既存を整える役。
- 書いた後の実装との追従ズレ点検は `doc-sync` に任せる。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] 記載した全コマンド・依存・設定キーを実装（scripts / pyproject / .env.example 等）から裏取りした
- [ ] Quick start のコマンドが通ることを確認した（最低限 scripts に存在することを確認）
- [ ] テンプレのプレースホルダ（`{{ }}`）が残っていない
- [ ] 既存 README があった場合、正確な既存記述を消していない
- [ ] 秘密情報・実値を書いていない（設定は .env.example を案内）

## 補足

- 詳細なトピックは README に詰め込まず `docs/` に分け、README からリンクする。
