# ビルドステージ
FROM python:3.11-bullseye AS build-stage

WORKDIR /app

RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient python-dotenv

COPY . .

# 実行ステージ
FROM python:3.11-bullseye AS production-stage

WORKDIR /app

COPY --from=build-stage /app/src /app/src

WORKDIR /app/src

CMD flask db upgrade && python run.py
