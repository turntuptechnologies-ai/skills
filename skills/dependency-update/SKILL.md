---
name: dependency-update
description: 依存パッケージ・ツールを更新するとき。「依存を上げて」「◯◯を最新にして」「dependabot/renovate の PR を処理して」「脆弱性対応して」等で使う。changelog と破壊的変更を確認し、影響箇所を調べてから更新し、pre-pr-checks で検証して PR にする。新規導入の「選定」は library-eval を使う。
---

# 依存更新（dependency-update）

## このスキルがやること

既存の依存を、破壊的変更を把握したうえで安全に更新する。「上げてみて動いたから OK」ではなく「何が変わるか読んでから上げる」。

## 手順

1. **対象と現在 → 目標バージョンを確認する**。stack 別の確認コマンド:

   | stack | 確認コマンド |
   |---|---|
   | Node/TS | `npm outdated` / `pnpm outdated` / `yarn outdated` |
   | Python (uv) | `uv tree --outdated`（無ければ `uv lock --upgrade` の lock diff で確認） |
   | Deno | `deno outdated` |
   | Rust | `cargo update --dry-run` |

2. **changelog / リリースノートを読む**: 現在 → 目標の間の全バージョンが対象。major 更新は BREAKING CHANGES を必読。changelog が無い場合は GitHub Releases・タグ間 diff を確認し、確認できた範囲と確認できなかった旨を報告する。
3. **影響を調べる**: 破壊的変更に挙がっている API・設定・挙動をコードベースで grep し、影響箇所を列挙する（影響なしなら「なし」と報告）。
4. **更新する**:
   - patch / minor → 複数まとめて更新してよい
   - **major → 1 パッケージずつ**（壊れたときに切り分けられる単位を保つ）。breaking 対応のコード修正は同じコミットに含める
5. **pre-pr-checks を実行する**（format / lint / typecheck / test）。
6. **PR にする**（create-pr）: 下記の報告表と、breaking 対応の内容・更新の目的を本文に書く。

## 報告フォーマット

必ずこの表で報告する:

```markdown
| パッケージ | 現在 → 更新後 | 種別 | breaking | 対応 |
|---|---|---|---|---|
| hono | 4.2.1 → 4.6.0 | minor | なし | — |
| tailwindcss | 3.4.0 → 4.0.2 | major | 設定が CSS-first に変更 | `tailwind.config.ts` を CSS へ移行 |
```

表の下に、更新の目的（脆弱性対応 / 必要機能 / 保守性）を 1 行書く。

## ルール・コツ

- **脆弱性起因**（`npm audit` / Dependabot alert 等）の更新は他より優先し、PR 本文に advisory（GHSA/CVE）を記載する。
- lockfile と依存宣言（package.json / pyproject.toml 等）を矛盾させない。lockfile だけの更新か宣言ごとの更新かを明示する。
- 更新後に壊れた場合、**すぐバージョンを戻さない**。まず原因（見落とした breaking change）を特定する。対応コストが大きく戻す判断をする場合はユーザーに確認する。
- 「更新のための更新」をしない。目的を報告に書けない更新は提案に留め、ユーザーに確認する。
- peer dependency の警告・エンジン要件（Node バージョン等）の変化も breaking として扱う。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] 更新した全パッケージを報告フォーマットの表（現在→更新後・種別・breaking・対応）で報告した
- [ ] major 更新は changelog / BREAKING CHANGES の確認結果と影響箇所の調査結果を報告した
- [ ] pre-pr-checks を実行し、結果を報告した
- [ ] major 更新を複数パッケージまとめて 1 コミットにしていない
- [ ] 更新の目的（脆弱性/機能/保守性）を報告に書いた

## 補足

- 社名・内部 URL・認証情報などの固有情報は扱わない。
- 新しい依存を「入れるかどうか・どれにするか」の判断は library-eval の領分。
