from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from app import db
from app.models import User, QuestionList, Question, Option

main_bp = Blueprint("main", __name__)


# Top ページ
@main_bp.route("/", methods=["GET"])
def index_get():
    if current_user.is_authenticated:
        question_lists = QuestionList.query.filter_by(creator_id=current_user.id).all()
        list_ids = [question_list.id for question_list in question_lists]
        list_titles = [question_list.list_title for question_list in question_lists]
    else:
        list_ids = []
        list_titles = []
    return render_template("index.html", list_ids=list_ids, list_titles=list_titles)


# 問題作成ページ
@main_bp.route("/question", methods=["GET"])
def create_question_get():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login_get"))
    return render_template("question.html")


# 問題作成 API
@main_bp.route("/question", methods=["POST"])
def create_question_post():
    form_data = request.form.to_dict()

    # JSON を変換
    json_data = {"list_title": form_data["list_title"], "question": {}}
    for key in form_data.keys():
        if key.startswith("question"):
            question_num = key.split("question")[1]
            question = {
                "question_text": form_data[key],
                "option": [],
                "answer": form_data["answer" + question_num],
            }
            for i in range(1, 5):
                option_key = "option" + question_num + "-" + str(i)
                if option_key in form_data:
                    question["option"].append(form_data[option_key])
            json_data["question"][question_num] = question

    # 問題リストの内容を格納
    creator_id = current_user.id
    list_title = json_data["list_title"]
    question_list = QuestionList(creator_id=creator_id, list_title=list_title)
    db.session.add(question_list)
    db.session.commit()

    # 問題の内容を格納
    list_id = question_list.id
    questions_data = json_data["question"]
    for key, question_data in questions_data.items():
        question_text = question_data["question_text"]
        correct_answer = question_data["answer"]
        question = Question(
            list_id=list_id, question_text=question_text, correct_answer=correct_answer
        )
        db.session.add(question)
        db.session.commit()

        # 問題の選択肢を格納
        question_id = question.id
        options_data = question_data["option"]
        for option_text in options_data:
            option = Option(question_id=question_id, option_text=option_text)
            db.session.add(option)
        db.session.commit()

    return redirect(url_for("main.question_content_get", list_id=list_id))


# 問題回答用 API
@main_bp.route("/question/<list_id>", methods=["GET"])
def question_content_get(list_id):
    question_list = QuestionList.query.get(list_id)
    if not question_list:
        return render_template("not_found.html")
    list_title = question_list.list_title
    questions = [question.question_text for question in question_list.questions]
    options = []
    for question in question_list.questions:
        question_options = [option.option_text for option in question.options]
        options.append(question_options)

    return render_template(
        "question_content.html",
        list_title=list_title,
        questions=questions,
        options=options,
    )


# DB リセット用 API
@main_bp.route("/reset", methods=["GET"])
def reset():
    db.session.query(Option).delete()
    db.session.query(Question).delete()
    db.session.query(QuestionList).delete()
    db.session.commit()

    return redirect(url_for("main.index_get"))
