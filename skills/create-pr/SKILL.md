---
name: create-pr
description: 変更をプルリクエスト(PR)として作成・提出するとき。「PR を作って」「プルリク出して」等と言われたら使う。デフォルトブランチへの直接 push を避け、ブランチ作成 → コミット → push → gh で PR 作成までを、Conventional Commits タイトルと定型の本文で一貫して行う。
---

# PR 作成手順

変更をレビュー可能な PR として提出する。**デフォルトブランチ（main/master）へ直接 push しない**ことを最優先で守る。

## 手順

1. **ブランチを確認・用意する**
   - 現在のブランチを確認: `git branch --show-current`
   - デフォルトブランチ（`main`/`master`）にいる場合は、作業用ブランチを切る:
     `git switch -c <type>/<short-desc>`（例: `feat/login-form`, `fix/null-crash`）
   - 既に作業ブランチにいればそのまま使う。

2. **変更をコミットする**
   - 関連する変更だけをステージ: `git add <paths>`（不要なら `git add -A`）
   - コミットメッセージは **Conventional Commits** 形式:
     `<type>: <要約>`（`feat`/`fix`/`docs`/`refactor`/`test`/`chore` など）
   - 要約は命令形・簡潔に。本文の言語はリポジトリ/Issue の慣習に合わせる。

3. **push する**
   - `git push -u origin <branch>`

4. **PR を作成する**
   - `gh pr create --title "<conventional title>" --body "<下記テンプレ>"`
   - タイトルも Conventional Commits 形式（例: `feat: ログインフォームを追加`）。
   - 対応する Issue があれば本文に `Closes #<N>` を入れる（merge 時に自動クローズ）。
   - 作成後、返ってきた PR の URL を報告する。

## PR 本文テンプレート

見出し構成は固定。プロ―ズ（説明文）の言語はリポジトリの慣習に合わせる。

```markdown
## 概要 / Summary
<この PR が何を・なぜ変えるか。1〜3 行>

## 変更点 / Changes
- <主要な変更を箇条書き>

## テスト / Testing
- <どう動作確認したか。未実施なら理由>

Closes #<N>   <!-- 対応 Issue があれば。なければ削除 -->
```

## タイトルの良い例 / 悪い例

| ✅ 良い | ❌ 悪い | 理由 |
|---|---|---|
| `fix: ログイン失敗時に null 参照でクラッシュする問題を修正` | `バグ修正` | type 無し・何のバグか不明 |
| `feat: CSV エクスポート機能を追加` | `feat: いろいろ更新` | 「いろいろ」は変更の主目的を表さない |
| `docs: README のセットアップ手順を現行コマンドに更新` | `fix: README 修正` | ドキュメントのみの変更は `docs`（`fix` はコード挙動の修正） |
| `refactor: 認証処理を middleware に集約（挙動変更なし）` | `feat: 認証まわり改善` | 挙動変更が無いなら `refactor` |

## ルール・コツ

- **main/master へ直接 push・直接コミットしない。** 必ずブランチ → PR を経由する。
- タイトルの `type` は変更の主目的に合わせる（バグ修正は `fix`、機能追加は `feat`、ドキュメントのみは `docs`）。複数種類が混ざる場合は主目的の type を選び、迷ったら分割を検討する。
- ステージ前に `git status` / `git diff --staged` で意図しない変更（秘密情報・生成物）が混ざっていないか確認する。
- リポジトリにブランチ保護や PR テンプレート（`.github/PULL_REQUEST_TEMPLATE.md`）があれば、それに従う。
- `gh` の認証が無い場合は `gh auth status` で確認し、ユーザーに案内する。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] 現在のブランチが main/master ではない（作業ブランチで commit している）
- [ ] コミットメッセージと PR タイトルが Conventional Commits 形式（`<type>: <説明>`）
- [ ] push 済みで、`gh pr create` が成功し **PR の URL を報告**した
- [ ] 対応 Issue がある場合、PR 本文に `Closes #N` が入っている
- [ ] PR 本文にテンプレの見出し（概要/変更点/テスト）が揃っている

## 補足

- 社名・内部 URL・認証情報などの固有情報はコミット/PR 本文に書かない。
