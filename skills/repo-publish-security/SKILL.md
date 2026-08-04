---
name: repo-publish-security
description: GitHub リポジトリを公開するとき（public で新規作成 / private から切替）や、公開リポジトリのセキュリティ設定を点検するとき。「リポジトリを公開して」「public にして」「公開前にセキュリティ設定を確認して」等で使う。secret scanning・Dependabot・ブランチ保護 ruleset・Actions 権限を gh CLI で点検し、不足分をユーザー確認の上で適用する。private → public 切替時は公開前に履歴の秘密情報チェックも行う。
---

# 公開リポジトリのセキュリティ設定

## このスキルがやること

GitHub リポジトリを公開するときに必要なセキュリティ設定を、gh CLI で点検し、不足分をユーザー確認の上で適用する。既存の公開リポジトリの定期点検にも使える。

## 手順

1. **対象と権限の確認**: `gh repo view --json nameWithOwner,visibility,viewerPermission`。設定変更には admin が必要。admin でなければ点検のみ行い、不足項目を管理者への依頼事項として報告する。
2. **private → public 切替の場合のみ**: 公開する**前に**、git 履歴を含めて秘密情報（API キー・トークン・内部 URL・個人情報）が無いか確認する。gitleaks 等のツールが使えれば使い、無ければ `git log -p` への代表的パターン（`api[_-]?key` / `token` / `secret` / `password` / `BEGIN .* PRIVATE KEY` 等）の grep と設定ファイルの目視で確認する。検出したら公開を中止し、該当秘密情報のローテーション（無効化・再発行）を先に行う（履歴の書き換えだけでは対策にならない）。
3. チェックリスト（下表）の全項目を確認欄の方法（コマンドまたはファイル有無の確認）で点検し、出力フォーマットの表で報告する。
4. 不足項目の適用可否をユーザーに確認し、了承された項目だけを適用コマンドで設定する。
5. 適用後、確認コマンドを再実行して反映を検証する。secret scanning を有効化した場合は、既存履歴の走査結果（open なアラートの件数）も確認する: `gh api --paginate "repos/{owner}/{repo}/secret-scanning/alerts?state=open&per_page=100" --jq '.[].number' | wc -l`

## チェックリスト

`{owner}/{repo}` は gh がカレントリポジトリから自動解決するので、リポジトリのルートでそのまま実行できる。

**基本**（すべての公開リポジトリ）:

| # | 項目 | 確認 | 適用 |
|---|---|---|---|
| 1 | Secret scanning + push protection | `gh api repos/{owner}/{repo} --jq .security_and_analysis` | 下記 JSON A を `gh api -X PATCH repos/{owner}/{repo} --input -` |
| 2 | Dependabot alerts | `gh api repos/{owner}/{repo}/vulnerability-alerts`（204=有効 / 404=無効） | `gh api -X PUT repos/{owner}/{repo}/vulnerability-alerts` |
| 3 | Actions の既定権限を read に | `gh api repos/{owner}/{repo}/actions/permissions/workflow` | `gh api -X PUT repos/{owner}/{repo}/actions/permissions/workflow -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false` |
| 4 | 各 workflow に最小権限の `permissions:` | `.github/workflows/` 配下の `*.yml` / `*.yaml` に `permissions:` ブロックがあるか grep | 各 workflow に必要最小の `permissions:`（例: `contents: read`）を追記 |
| 5 | デフォルトブランチ保護 ruleset（削除・force push 禁止 + PR 必須） | `gh api repos/{owner}/{repo}/rulesets` | 下記 JSON B を `gh api -X POST repos/{owner}/{repo}/rulesets --input -` |
| 6 | squash マージのみ + マージ後ブランチ自動削除 | `gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge` | `gh repo edit --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false --delete-branch-on-merge` |

**推奨**（継続的にメンテするリポジトリ・プロダクト。単発のデモ等では見送り可）:

| # | 項目 | 確認 | 適用 |
|---|---|---|---|
| 7 | Dependabot security updates | `gh api repos/{owner}/{repo}/automated-security-fixes` | `gh api -X PUT repos/{owner}/{repo}/automated-security-fixes` |
| 8 | Private vulnerability reporting（脆弱性の非公開報告窓口） | `gh api repos/{owner}/{repo}/private-vulnerability-reporting` | `gh api -X PUT repos/{owner}/{repo}/private-vulnerability-reporting` |
| 9 | CI を required status check に | #5 の ruleset 確認結果に `required_status_checks` rule があるか | JSON B の直後に示す追加 rule を ruleset に入れる（→ JSON B 下の説明） |
| 10 | `dependabot.yml`（依存の version updates） | `.github/dependabot.yml` の有無 | エコシステムに合わせて作成（週次が目安） |
| 11 | `SECURITY.md`（任意） | `SECURITY.md` / `.github/SECURITY.md` の有無 | 報告手順を記載。#8 を有効にした場合はリポジトリの Security タブの報告フォームへ誘導する |

JSON A — secret scanning + push protection:

```json
{"security_and_analysis": {
  "secret_scanning": {"status": "enabled"},
  "secret_scanning_push_protection": {"status": "enabled"}
}}
```

JSON B — デフォルトブランチ保護 ruleset:

```json
{"name": "main-protection", "target": "branch", "enforcement": "active",
 "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
 "rules": [
   {"type": "deletion"},
   {"type": "non_fast_forward"},
   {"type": "pull_request", "parameters": {
     "allowed_merge_methods": ["squash"],
     "required_approving_review_count": 0,
     "dismiss_stale_reviews_on_push": false,
     "require_code_owner_review": false,
     "require_last_push_approval": false,
     "required_review_thread_resolution": false}}
 ]}
```

CI を required status check にする場合（#9）の追加 rule（`context` は実際の check 名に合わせる）:

```json
{"type": "required_status_checks", "parameters": {
  "required_status_checks": [{"context": "ci"}],
  "strict_required_status_checks_policy": false}}
```

新規作成ならこれを JSON B の `rules` に含めて POST する。**既存 ruleset への追加は POST を再実行しない**（重複 ruleset ができる）。`gh api repos/{owner}/{repo}/rulesets --jq '.[].id'` で id を取り、rule を足した ruleset 全体を `gh api -X PUT repos/{owner}/{repo}/rulesets/<id> --input -` で送り直す。

## 出力フォーマット（点検結果）

| 項目 | 区分 | 現状 | 判定 |
|---|---|---|---|
| Secret scanning + push protection | 基本 | enabled | OK |
| デフォルトブランチ保護 ruleset | 基本 | なし | 不足 |
| Dependabot security updates | 推奨 | disabled | 見送り（単発デモのため） |

判定は OK / 不足 / 見送り（理由付き）/ 対象外（理由付き）の 4 値。適用後は「適用結果」列を足して再掲する。

## ルール・コツ

- **点検結果の提示 → ユーザー了承 → 適用**の順を守る。特に ruleset は既存の運用（デフォルトブランチへの直 push 等）を止めるので、黙って適用しない。
- JSON B の `required_approving_review_count` は運用に合わせて確認する: 1 人運用・AI エージェントがセルフマージする運用なら 0、複数人レビュー運用なら 1 以上。
- 既に classic branch protection（`gh api repos/{owner}/{repo}/branches/<default branch>/protection`）で同等の保護がある場合、ruleset を重ねて作らない。
- private のままだと有効化できない項目がある（secret scanning 等は private では GitHub Advanced Security 契約が必要）。private → public 切替では「切替 → 直後に適用」の順で進める。
- fork や archive 済みリポジトリでは変更できない設定がある。エラーになった項目は対象外として理由を報告する。
- 新規プロジェクトの立ち上げなら `new-project-init` を先に使い、本 Skill はリポジトリを GitHub に公開する段階で使う（ローカル側の main 保護 hook はあちら、サーバ側の強制はこちら）。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] チェックリスト全 11 項目の現状を確認し、点検結果表で報告した
- [ ] 不足項目は適用可否をユーザーに確認し、了承された項目のみ適用した（見送り・対象外は理由を表に記録した）
- [ ] 適用した項目は確認コマンドの再実行で反映を検証した
- [ ] private → public 切替の場合、公開前に git 履歴を含む秘密情報の確認を実施した（検出時は公開を中止し、ローテーションを先行した）
- [ ] secret scanning を新規に有効化した場合、既存アラートの件数を確認して報告した

## 補足

- 社内固有情報（社名・内部 URL・認証情報など）は書かない。対象リポジトリは gh の `{owner}/{repo}` プレースホルダで解決する。
- org 全体で新規リポジトリに自動適用したい設定が出てきたら、org の設定（Code security の default 設定）や organization ruleset への昇格を検討する（本 Skill はリポジトリ単位）。
