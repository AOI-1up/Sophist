FROM python:3.11-bullseye

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080