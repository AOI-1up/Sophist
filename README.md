# Sophist
## 開発環境の起動
事前に `.env` をダウンロードしておくこと。
```
> git clone https://github.com/AOI-1up/Sophist.git
> copy .env Sophist/
> cd Sophist/
> docker compose up -d
> docker exec -it app bash
# cd src/
# python run.py
```

## マイグレーション (初期起動時)
```
> docker exec -it app bash
# cd src/
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
```
