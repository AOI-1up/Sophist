from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


# Top ページ用 API
@main_bp.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")


# 問題作成用 API
@main_bp.route("/question", methods=["GET"])
def create_question_get():
    return render_template("question.html")
