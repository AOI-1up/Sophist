from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ユーザモデルを定義
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    # パスワードをハッシュ化し格納するメソッドを定義
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # パスワードの一致を確認するメソッドを定義
    def check_password(self, password):
        return check_password_hash(self.password, password)
