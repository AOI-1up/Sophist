from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from app import db
from app.models import QuestionList, Question, Option

main_bp = Blueprint("main", __name__)


# Top ページ用 API
@main_bp.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")


# 問題作成用 API
@main_bp.route("/question", methods=["GET"])
def create_question_get():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login_get"))
    return render_template("question.html")


@main_bp.route("/question", methods=["POST"])
def create_question_post():
    form_data = request.form.to_dict()

    # 問題リストの内容を格納
    creator_id = current_user.id
    list_title = form_data.get("list_title")
    question_list = QuestionList(creator_id=creator_id, list_title=list_title)
    db.session.add(question_list)
    db.session.commit()

    # 問題の内容を格納
    list_id = question_list.id
    question_keys = [key for key in form_data.keys() if key.startswith("question")]
    answer_list = [key for key in form_data.keys() if key.startswith("answer")]
    for key in question_keys:
        question_text = form_data.get(key)
        correct_answer = form_data.get(answer_list[question_keys.index(key)])
        question = Question(
            list_id=list_id, question_text=question_text, correct_answer=correct_answer
        )
        db.session.add(question)
    db.session.commit()

    # 選択肢の内容を格納
    question_id = question.id
    option_keys = [key for key in form_data.keys() if key.startswith("option")]
    for key in option_keys:
        option_text = form_data.get(key)
        option = Option(question_id=question_id, option_text=option_text)
        db.session.add(option)
    db.session.commit()

    return redirect(url_for("main.question_content_get", list_id=list_id))


# 問題回答用 API
@main_bp.route("/question/<list_id>", methods=["GET"])
def question_content_get(list_id):
    list = QuestionList.query.get(list_id)
    list_title = list.list_title
    return render_template(
        "question_content.html", list_title=list_title
    )
