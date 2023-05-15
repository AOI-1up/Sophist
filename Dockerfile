FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src/app.py app.py
COPY ./src/templates templates

EXPOSE 8080

CMD ["python", "app.py"]