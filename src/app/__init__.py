from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# オブジェクトをグローバルスコープで宣言
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

# Flask アプリケーションを初期化
def create_app():
    app = Flask(__name__)

    # SQLAlchemy 用の認証・接続情報を定義
    load_dotenv()
    DB_USER = os.environ['MYSQL_USER']
    DB_PASS = os.environ['MYSQL_PASSWORD']
    DB_HOST = "db"
    DB_NAME = os.environ['MYSQL_DATABASE']

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = "secret"

    # Flask アプリケーションと拡張機能を結合
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Blueprint オブジェクトをインポート
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .models import User

    # オブジェクトを Flask アプリケーションに登録
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # ユーザ情報をロード
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app