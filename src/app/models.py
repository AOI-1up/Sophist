from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ユーザのモデルを定義
class User(UserMixin, db.Model):
    __tablename__ = "user"
    # ユーザ ID (主キー)
    id = db.Column(db.Integer, primary_key=True)

    # 名前
    name = db.Column(db.String(128))
    # メールアドレス
    mail = db.Column(db.String(128), unique=True)
    # パスワード
    password = db.Column(db.String(128))

    # 問題作成者との関係
    creator = db.relationship("QuestionList", backref="user", lazy=True)
    # 問題回答者との関係
    answerer = db.relationship("AnswerResult", backref="user", lazy=True)
    # インポート・ブックマークとの関係
    import_user = db.relationship("ImportList", backref="user", lazy=True)
    bookmark_user = db.relationship("BookmarkList", backref="user", lazy=True)

    # パスワードをハッシュ化し格納するメソッドを定義
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # パスワードの一致を確認するメソッドを定義
    def check_password(self, password):
        return check_password_hash(self.password, password)


# 問題リストのモデルを定義
class QuestionList(db.Model):
    __tablename__ = "question_list"
    # 問題リスト ID (主キー)
    id = db.Column(db.Integer, primary_key=True)
    # 作成者 ID (外部キー)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # 問題リストのタイトル
    list_title = db.Column(db.String(128))

    # 問題との関係
    questions = db.relationship("Question", backref="question_list", lazy=True)
    # 回答結果との関係
    answer_results = db.relationship("AnswerResult", backref="question_list", lazy=True)
    # インポート・ブックマークとの関係
    import_list = db.relationship("ImportList", backref="question_list", lazy=True)
    bookmark_list = db.relationship("BookmarkList", backref="question_list", lazy=True)


# 問題のモデルを定義
class Question(db.Model):
    __tablename__ = "question"
    # 問題 ID (主キー)
    id = db.Column(db.Integer, primary_key=True)
    # 選択肢が属する問題の ID (外部キー)
    list_id = db.Column(db.Integer, db.ForeignKey("question_list.id"), nullable=False)

    # 問題の内容
    question_text = db.Column(db.String(128))
    # 正解の選択肢
    correct_answer = db.Column(db.Integer)

    # 選択肢との関係
    options = db.relationship("Option", backref="question", lazy=True)
    # 回答結果との関係
    answer_results = db.relationship("AnswerResult", backref="question", lazy=True)


# 選択肢モデルを定義
class Option(db.Model):
    __tablename__ = "option"
    # 選択肢 ID (主キー)
    id = db.Column(db.Integer, primary_key=True)
    # 選択肢が属する問題の ID (外部キー)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    # 選択肢の内容
    option_text = db.Column(db.String(128))


# 回答結果モデルを定義
class AnswerResult(db.Model):
    __tablename__ = "answer_result"
    # 回答結果 ID (主キー)
    id = db.Column(db.Integer, primary_key=True)
    # 回答者の ID (外部キー)
    answerer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # 回答した問題リストの ID (外部キー)
    list_id = db.Column(db.Integer, db.ForeignKey("question_list.id"), nullable=False)
    # 回答した問題の ID (外部キー)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    # 回答結果の内容
    user_answer = db.Column(db.Integer)


# インポートモデルを定義
class ImportList(db.Model):
    __tablename__ = "import_list"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("question_list.id"), nullable=False)


# ブックマークモデルを定義
class BookmarkList(db.Model):
    __tablename__ = "bookmark_list"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("question_list.id"), nullable=False)
