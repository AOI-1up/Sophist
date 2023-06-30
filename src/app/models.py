from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ユーザのモデルを定義
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)    # ユーザ ID (主キー)
    name = db.Column(db.String(128))                # 名前
    mail = db.Column(db.String(128), unique=True)   # メールアドレス
    password = db.Column(db.String(128))            # パスワード
    creator = db.relationship(                      # 問題との関係
        'QuestionList',
        backref='user',
        lazy=True
    )

    # パスワードをハッシュ化し格納するメソッドを定義
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # パスワードの一致を確認するメソッドを定義
    def check_password(self, password):
        return check_password_hash(self.password, password)


# 問題リストのモデルを定義
class QuestionList(db.Model):
    __tablename__ = 'question_list'
    id = db.Column(db.Integer, primary_key=True)    # 問題リスト ID (主キー)
    creator_id = db.Column(                         # 作成者 ID (外部キー)
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    list_title = db.Column(db.String(128))          # 問題リストのタイトル
    questions = db.relationship(                    # 問題との関係 (1:多)
        'Question',
        backref='question_list',
        lazy=True
    )


# 問題のモデルを定義
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)    # 問題 ID (主キー)
    list_id = db.Column(                            # 選択肢が属する問題の ID (外部キー)
        db.Integer,
        db.ForeignKey('question_list.id'),
        nullable=False
    )
    question_text = db.Column(db.String(128))       # 問題の内容
    options = db.relationship(                      # 選択肢との関係 (1:多)
        'Option',
        backref='question',
        lazy=True
    )
    correct_answer = db.Column(db.Integer)          # 正解の選択肢


# 選択肢モデルを定義
class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key=True)    # 選択肢 ID (主キー)
    question_id = db.Column(                        # 選択肢が属する問題の ID (外部キー)
        db.Integer,
        db.ForeignKey('question.id'),
        nullable=False
    )
    option_text = db.Column(db.String(128))         # 選択肢の内容
