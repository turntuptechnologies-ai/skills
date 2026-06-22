---
description: ブランチ運用の制約
---

- `main` / `master` へ直接コミット・直接 push しない
- 変更は Issue → `issue-<番号>/<説明>` ブランチ → PR（`Closes #N`）→ squash merge → ブランチ削除 の順で行う
- この制約は指示だけに頼らず、フック（`block-main-push.sh`）と GitHub のブランチ保護で担保する
