# ビルドステージ
FROM python:3.11-bullseye AS build-stage

WORKDIR /app

# 依存パッケージのインストール
RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient python-dotenv

# ソースコードのコピー
COPY . .

# ビルドステージでのビルドコマンドは不要なため省略

# 実行ステージ
FROM python:3.11-bullseye AS production-stage

WORKDIR /app

# 依存パッケージのインストール
RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient python-dotenv

# ソースコードのコピー（ビルドステージからコピー）
COPY --from=build-stage /app/src /app/src

WORKDIR /app/src

# データベースの初期化、マイグレーション、アップグレードの実行
# RUN flask db migrate && flask db upgrade

# アプリケーションの起動
CMD flask db upgrade && python run.py
