from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ユーザモデルを定義
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)    # ユーザ ID (主キー)
    name = db.Column(db.String(128))                # 名前
    mail = db.Column(db.String(128), unique=True)   # メールアドレス
    password = db.Column(db.String(128))            # パスワード
    creator = db.relationship(
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


# 問題リストモデルを定義
class QuestionList(db.Model):
    __tablename__ = 'question_list'
    id = db.Column(db.Integer, primary_key=True)    # 問題リスト ID (主キー)
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    questions = db.relationship(
        'Question',
        backref='question_list',
        lazy=True
    )


# 問題モデルを定義
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


"""
# 問題リストモデルを定義
class QuestionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # 問題リストID（主キー）
    list_title = db.Column(db.String(128))          # 問題リストのタイトル
    creator_id = db.Column(                         # 作成者のユーザID（外部キー）
        db.Integer,
        db.ForeignKey(User.id)
    )
    creator = db.relationship(                          # 作成者とのリレーション
        User,
        backref=db.backref('question_lists', lazy=True)
    )



# 問題モデルを定義
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)   # 問題ID（主キー）
    question_content = db.Column(db.String(128))            # 問題のタイトル
    choices = db.relationship(                              # 選択肢とのリレーション
        'Choice',
        backref=db.backref('question', lazy=True)
    )
    correct_answer = db.relationship(                       # 正解とのリレーション
        'CorrectAnswer',
        backref=db.backref('question', uselist=False),
    )
    question_list_id = db.Column(                           # 問題リストID（外部キー）
        db.Integer,
        db.ForeignKey('question_list.id')
    )


# 解答結果モデルを定義
class AnswerResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # 解答結果ID（主キー）
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))                                         # ユーザID（外部キー）
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.question_id'))                            # 問題ID（外部キー）
    selected_choice = db.Column(db.String(128))             # 選んだ選択肢


# 選択肢モデルを定義
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # 選択肢ID（主キー）
    question_id = db.Column(db.Integer, db.ForeignKey(      # 問題ID（外部キー）
        'question.question_id'))
    choice_text = db.Column(db.String(128))                 # 選択肢のテキスト


# 正解モデルを定義
class CorrectAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)             # 正解ID（主キー）
    question_id = db.Column(db.Integer, db.ForeignKey(              # 問題ID（外部キー）
        'question.question_id'))
    choice_id = db.Column(db.Integer, db.ForeignKey(                # 選択肢ID（外部キー）
        'choice.choice_id'))
    question_rel = db.relationship(
        'Question',
        backref=db.backref('correct_answer_rel', uselist=False),
        overlaps="correct_answer"
    )
    # 選択肢とのリレーション
    choice = db.relationship('Choice')
"""
