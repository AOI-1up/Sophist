from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ユーザモデルを定義
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)    # ユーザID（主キー）
    name = db.Column(db.String(128))                # 名前
    mail = db.Column(db.String(128), unique=True)   # メールアドレス
    password = db.Column(db.String(128))            # パスワード

    # パスワードをハッシュ化し格納するメソッドを定義
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # パスワードの一致を確認するメソッドを定義
    def check_password(self, password):
        return check_password_hash(self.password, password)


# 解答結果モデルを定義
class AnswerResult(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)     # 解答結果ID（主キー）
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))                                         # ユーザID（外部キー）
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.question_id'))                            # 問題ID（外部キー）
    selected_choice = db.Column(db.String(128))             # 選んだ選択肢


# 問題リストモデルを定義
class QuestionList(db.Model):

    list_id = db.Column(db.Integer, primary_key=True)       # 問題リストID（主キー）
    list_title = db.Column(db.String(128))                  # 問題リストのタイトル
    creator_id = db.Column(db.Integer, db.ForeignKey(       # 作成者のユーザID（外部キー）
        'user.id'))
    creator = db.relationship('User', backref=db.backref(   # 作成者とのリレーション
        'question_lists', lazy=True))


# 問題モデルを定義
class Question(db.Model):

    question_id = db.Column(db.Integer, primary_key=True)       # 問題ID（主キー）
    question_title = db.Column(db.String(128))                  # 問題のタイトル
    choices = db.relationship(                                  # 選択肢とのリレーション
        'Choice', backref='question', lazy=True)
    correct_answer = db.relationship(                           # 正解とのリレーション
        'CorrectAnswer', uselist=False)
    question_list_id = db.Column(db.Integer, db.ForeignKey(     # 問題リストID（外部キー）
        'question_list.list_id'))


# 選択肢モデルを定義
class Choice(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)     # 選択肢ID（主キー）
    question_id = db.Column(db.Integer, db.ForeignKey(      # 問題ID（外部キー）
        'question.question_id'))
    choice_text = db.Column(db.String(128))                 # 選択肢のテキスト


# 正解モデルを定義
class CorrectAnswer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)             # 正解ID（主キー）
    question_id = db.Column(db.Integer, db.ForeignKey(              # 問題ID（外部キー）
        'question.question_id'))
    choice_id = db.Column(db.Integer, db.ForeignKey(                # 選択肢ID（外部キー）
        'choice.choice_id'))
    question_rel = db.relationship('Question', backref=db.backref(  # 問題とのリレーション
        'correct_answer_rel', uselist=False))
    choice = db.relationship('Choice')                              # 選択肢とのリレーション
