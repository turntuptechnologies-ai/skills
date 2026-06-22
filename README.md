# skills

社内で共有して使う [Claude Code](https://claude.com/claude-code) の **Skill** 置き場。

将来的に社外 OSS 公開も視野に入れているため、各 Skill は **社内固有情報を一切含めず、汎用的に動く**ように書く（→ [運用ルール](#運用ルール)）。

## Skill とは

特定の作業のやり方を Claude に教える「手順書フォルダ」。実体は `SKILL.md`（Markdown + フロントマター）1 ファイル。

```
skills/<skill-name>/
  └── SKILL.md      ← 本体
  └── (任意) 補助スクリプト・参考資料
```

## 使い方（各メンバー）

このリポジトリを clone し、使いたい Skill を自分の Claude 環境から見えるようにする。

```bash
git clone https://github.com/turntuptechnologies-ai/skills.git
cd skills

# 例: 個人環境(~/.claude/skills)へシンボリックリンク
ln -s "$(pwd)/skills/<skill-name>" ~/.claude/skills/<skill-name>

# またはプロジェクト単位で使うなら .claude/skills/ にリンク/コピー
```

`description` を見て Claude が自動的に使うか判断する。明示的に呼びたいときは `/<skill-name>`。

## 新しい Skill を追加する

1. `skills/<skill-name>/SKILL.md` を作る（雛形は [`templates/SKILL.md`](templates/SKILL.md)）
2. ローカルで試して `description` と手順を調整
3. ブランチを切って PR（→ [運用ルール](#運用ルール)）

## 運用ルール

- **社内固有情報を書かない** — 社名・組織名・内部 URL・認証情報・固有プロジェクト名を Skill 本文に埋め込まない。環境差は環境変数や引数で渡す。公開時に履歴を漁られても問題ない状態を最初から保つ。
- **1 Skill = 1 ディレクトリ**、`SKILL.md` 必須。
- **`description` が命** — 「いつ使うか・何をするか」を具体的に書く。これで発動可否が決まる。
- main 直 push 禁止。Issue → ブランチ → PR → merge。
