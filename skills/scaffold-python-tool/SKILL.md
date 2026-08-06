---
name: scaffold-python-tool
description: Python の CLI ツールやバックエンドサービスを新規に作るとき。「Python のツールを作る」「uv でプロジェクト初期化」等で使う。uv + ruff + mypy(strict) + pytest の構成で雛形を用意する（任意で FastAPI / SQLAlchemy / click）。土台は new-project-init を先に使う。
---

# Python ツール scaffold（uv + ruff + mypy + pytest）

src レイアウトの Python プロジェクトを雛形生成する。

## stack

- Python **3.12+**、パッケージ管理 **uv**、ビルド **hatchling**
- レイアウト: **src/**（`src/<pkg>/`）
- lint/format: **ruff**、型チェック: **mypy（strict）**、テスト: **pytest**（+`pytest-asyncio`）
- よく足すもの: `click`(CLI) / `pydantic` / `fastapi`+`uvicorn` / `sqlalchemy`(async)+`alembic` / `httpx` / `pyyaml`

## 手順

1. **初期化**
   ```bash
   uv init --package --name <pkg> .   # src レイアウトのパッケージとして初期化
   ```
2. **依存を追加**（必要なものだけ）
   ```bash
   uv add pydantic click pyyaml httpx          # 例
   uv add fastapi "uvicorn[standard]"           # API を作るなら
   uv add sqlalchemy aiosqlite alembic          # DB を使うなら（PostgreSQL は asyncpg）
   uv add --dev ruff mypy pytest pytest-asyncio
   ```
3. **`pyproject.toml` に設定を足す**
   ```toml
   [project.scripts]
   <pkg> = "<pkg>.cli:main"        # CLI なら

   [tool.ruff]
   target-version = "py312"
   src = ["src", "tests"]
   [tool.ruff.lint]
   select = ["E", "F", "W", "I", "UP", "B", "SIM", "TCH"]

   [tool.mypy]
   python_version = "3.12"
   strict = true
   packages = ["<pkg>"]
   mypy_path = "src"

   [tool.pytest.ini_options]
   testpaths = ["tests"]
   ```
4. **ディレクトリ**: `src/<pkg>/`（`cli.py`, `__init__.py` 等）、`tests/`。
5. **動作確認**
   ```bash
   uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
   ```
   （`pre-pr-checks` Skill がこの一括実行を担う）

## ルール・コツ

- **mypy は strict 前提**で書く。型注釈を最初から付ける。
- async コードのテストは `pytest-asyncio`。設定は `asyncio_mode = "auto"` が楽。
- DB マイグレーションは alembic（`alembic init` → `alembic.ini` の `sqlalchemy.url` を設定/環境変数化）。
- 秘密情報は `.env`＋`python-dotenv`、コミットするのは `.env.example` のみ。
- ランタイムは mise で固定、sudo は使わない。

## 完了条件

以下を全て満たしたら完了。**満たせない項目があれば、黙って省略せず理由を報告する。**

- [ ] src レイアウト（`src/<pkg>/`, `tests/`）で `uv sync` が通る
- [ ] pyproject に ruff / mypy(strict) / pytest の設定が入っている
- [ ] `uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest` が通る
- [ ] CLI がある場合 `[project.scripts]` が定義されている
- [ ] `.env` はコミット対象外、`.env.example` のみ（実値なし）

## 補足

- ライセンスは permissive（MIT 等）前提。GPL 系依存は避ける。
- 記載のバージョン・パッケージ構成は Skill 作成時点の目安。初期化時に最新安定版を確認して読み替える。
