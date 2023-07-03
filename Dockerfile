FROM python:3.11-bullseye

RUN pip install Flask==2.2.3 Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient python-dotenv

WORKDIR /src
COPY . .

EXPOSE 8080

CMD python src/run.py && flask db init && flask db migrate && flask db upgrade