# ビルドステージ
FROM python:3.11-bullseye

RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient python-dotenv

WORKDIR /app
COPY . .

WORKDIR /app/src
CMD flask db upgrade && python run.py
