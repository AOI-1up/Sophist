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


# 問題モデルを定義
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(128))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship(
        'User', backref=db.backref('questions', lazy=True))


# 選択肢モデルを定義
class Choice(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    choice_text = db.Column(db.String(128))
    question = db.relationship(
        'Question', backref=db.backref('choices', lazy=True))


# 正解モデルを定義
class CorrectAnswer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.choice_id'))
    question = db.relationship(
        'Question', backref=db.backref('correct_answer', uselist=False))
    choice = db.relationship('Choice')
