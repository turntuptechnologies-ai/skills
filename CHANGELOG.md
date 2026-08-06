# Changelog

このリポジトリの主な変更を記録する。形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に従い、バージョンは [Semantic Versioning](https://semver.org/lang/ja/) に従う。

## [0.2.0] - 2026-08-06

公開リポジトリのセキュリティ設定を点検・適用する新 Skill `repo-publish-security` を追加（Skill は 23 個に）。`handoff` はセッションを閉じて開き直した場合も自動復元されるようになり、Skill の品質は CI の機械検査と skill-lint のコマンド実行検証で二重に守られるようになった。

### Added

- `repo-publish-security` — リポジトリ公開時のセキュリティ設定（secret scanning / Dependabot / ブランチ保護 ruleset / Actions 権限）を gh CLI で点検し、ユーザー確認の上で適用する。private → public 切替時は公開前に git 履歴の秘密情報チェックを行う (#73, #74)
- `skill-lint` にチェック項目 10「コマンドの実行検証」を追加。副作用のない確認系コマンドは実際に実行して確かめ、実行できない場合は未検証として理由を報告する (#77, #81)
- Skill 構造の機械検査 `scripts/lint-skills.py` と GitHub Actions CI を追加。frontmatter・必須節・完了条件の前文・曖昧語・README カタログ同期を PR ごとに検査し、required status check として必須化 (#78, #82)
- `handoff` の初回保存時に、`.claude/handoff/` を git 管理から除外する方法（`.gitignore` / `.git/info/exclude` / 何もしない）を確認するようにした (#72)

### Changed

- `handoff` の SessionStart hook が新しいセッションの開始時（`startup`）にも発動し、セッションを閉じて開き直した場合（日またぎ等）も引き継ぎ書が自動復元されるようになった。`--resume`・`--continue` での会話再開は対象外 (#79, #83)
- `handoff` の保存提案トリガーを見直し、`run-agent-team` の Subagents フォールバックにロール別の reasoning effort 指針を追加 (#70)
- Skill 間の整合性を改善 — `new-project-init` から `repo-publish-security` への導線、調査系 Skill の `deep-research` 非対応環境向けフォールバック、scaffold 系への「記載バージョンは作成時点の目安」注記、全 Skill の節順統一（完了条件 → 補足） (#80, #84)

### Fixed

- `repo-publish-security` の secret scanning アラート件数コマンドが gh の仕様（`--slurp` と `--jq` の併用不可）で実行できなかった問題を修正 (#75, #76)

## [0.1.0] - 2026-07-26

初回リリース。`turntup` プラグインを install すると、Issue 起票 → 実装 → 品質ゲート → PR → リリースまでの開発フローを 22 個の Skill として呼び出せる。

### Added

#### 配布とパッケージング

- Claude Code プラグイン `turntup`（マーケットプレイス `turntup-skills`）として配布。`/plugin marketplace add turntuptechnologies-ai/skills` で登録し、`/turntup:<skill-name>` で各 Skill を呼べる (#28)
- `handoff` 用の hook を同梱。セッション開始時に引き継ぎ書を自動で読み込み、compact 時に要点を保持する
- MIT LICENSE と、インストール手順・スキルカタログ・運用ルールを載せた README (#63, #67)

#### プロジェクト立ち上げ

- `new-project-init` — フェーズ制・Conventional Commits・Issue → PR フローを定めた CLAUDE.md、常時効かせる Rules、main 保護フックを揃える (#6, #14)
- `scaffold-cf-worker` — Cloudflare Workers（wrangler + Hono + TypeScript + Vitest + Biome）の雛形 (#22)
- `scaffold-deno-api` — Deno API サーバー（Hono + Drizzle ORM + PostgreSQL）の雛形 (#24)
- `scaffold-python-tool` — Python CLI / バックエンド（uv + ruff + mypy strict + pytest）の雛形 (#10)
- `scaffold-react-app` — React SPA（Vite + TypeScript + Tailwind v4 + Vitest）の雛形 (#12)
- `scaffold-wxt-extension` — ブラウザ拡張（WXT + React + TypeScript + Tailwind v4）の雛形 (#8)

#### 実装と品質ゲート

- `pre-pr-checks` — stack を自動判定し format / lint / typecheck / test を正しいコマンドで一括実行する (#4)
- `debug-root-cause` — 再現 → 切り分け → 根本原因特定 → 回帰テスト → 修正 → 水平展開の順で進め、対症療法で終わらせない (#55)
- `dependency-update` — changelog と破壊的変更を確認し、影響箇所を調べてから依存を更新する (#56)
- `adversarial-verify` — 結論を別視点から反証させて、もっともらしいだけの指摘を落とす (#59)

#### Issue・PR・リリース

- `create-issue` — 重複を検索したうえで、背景・提案・受け入れ条件の定型テンプレで Issue を作成する (#52)
- `create-pr` — デフォルトブランチへの直接 push を避け、ブランチ作成 → コミット → push → PR 作成までを一貫して行う (#2)
- `pr-babysit` — PR の checks を監視し、失敗したらログから原因を特定して green になるまで直す (#54)
- `release` — 前回タグからの変更を集め、Conventional Commits から semver でバージョンを決めて CHANGELOG・タグ・GitHub Release まで行う (#57)

#### ドキュメントとセッション運用

- `doc-sync` — 変更差分から影響しうるドキュメントを洗い出し、実装との食い違いを点検して直す (#18)
- `write-readme` — 実装から裏を取りつつ、実証済みの構成で README を書く (#20)
- `handoff` — 作業のゴール・進捗・重要ファイル・決定事項を `.claude/handoff/latest.md` に保存し、新セッションで再開できるようにする

#### 調査

- `library-eval` — 候補ライブラリを保守状況・採用度・ライセンス・脆弱性・API 適合で比較し、推奨とリスクを出す (#36)
- `literature-review` — 複数の学術ソースから論文を選別し、引用付きのレビューと研究ギャップにまとめる (#32)
- `market-research` — 市場規模・競合・トレンド・価格・リスクを出典付きの構造化レポートにまとめる (#34)

#### Skill 運用と Agent Teams

- `skill-lint` — frontmatter・構成・完了条件の検証可能性・固有情報の混入・カタログ追記漏れを検査し、修正案付きで指摘する (#53)
- `run-agent-team` — architect → reviewer → developer → tester → documenter を編成し、タスク依存で進めて解散前チェックまで回す。解散前チェックは実装に関与していないエージェントが担当する (#26, #44)
- `run-agent-team` に TeamCreate が使えない環境向けの Subagents フォールバックを追加 (#61)

#### 全 Skill 共通

- 各 Skill に、満たせない項目があれば理由を報告させる完了条件チェックリストを追加 (#40)
- 各 Skill に出力フォーマットの明示と良い例 / 悪い例を追加 (#42)

[0.2.0]: https://github.com/turntuptechnologies-ai/skills/releases/tag/v0.2.0
[0.1.0]: https://github.com/turntuptechnologies-ai/skills/releases/tag/v0.1.0
