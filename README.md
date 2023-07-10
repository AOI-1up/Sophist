# Sophist
## ブランチの定義
- main: 開発 (Docker) 環境
- production: 本番 (Kubernetes) 環境


## 開発環境の起動
```
> git clone https://github.com/AOI-1up/Sophist.git
> cd Sophist/
> vim .env
MYSQL_ROOT_PASSWORD = "{{ root パスワード }}"
MYSQL_DATABASE = "{{ データベース名 }}"
MYSQL_USER = "{{ ユーザ名 }}"
MYSQL_PASSWORD = "{{ パスワード }}"
> docker compose up -d
> docker exec -it app bash
# cd src/
# python run.py
```

### マイグレーション (初回起動時)
```
> docker exec -it app bash
# cd src/
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
```


## Kubernetes 環境の起動
```
$ git clone https://github.com/AOI-1up/Sophist.git
$ cd Sophist/
$ git checkout production
$ kubectl apply -f ./manifests/
```
