from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from app import db
from app.models import (
    User,
    QuestionList,
    Question,
    Option,
    AnswerResult,
    ImportList,
    BookmarkList,
)

main_bp = Blueprint("main", __name__)


# Top ページ
@main_bp.route("/", methods=["GET"])
def index_get():
    if current_user.is_authenticated:
        created_lists = QuestionList.query.filter_by(creator_id=current_user.id).all()
        created_list_ids = [created_list.id for created_list in created_lists]
        created_list_titles = [
            question_list.list_title for question_list in created_lists
        ]

        imported_lists = ImportList.query.filter_by(user_id=current_user.id).all()
        imported_list_ids = [imported_list.list_id for imported_list in imported_lists]
        imported_list_titles = [
            QuestionList.query.get(imported_list.list_id).list_title
            for imported_list in imported_lists
        ]

        bookmarked_lists = BookmarkList.query.filter_by(user_id=current_user.id).all()
        bookmarked_list_ids = [
            bookmarked_list.list_id for bookmarked_list in bookmarked_lists
        ]
        bookmarked_list_titles = [
            QuestionList.query.get(bookmarked_list.list_id).list_title
            for bookmarked_list in bookmarked_lists
        ]

    else:
        created_list_ids = []
        created_list_titles = []
        imported_list_ids = []
        imported_list_titles = []
        bookmarked_list_ids = []
        bookmarked_list_titles = []

    return render_template(
        "index.html",
        created_list_ids=created_list_ids,
        created_list_titles=created_list_titles,
        imported_list_ids=imported_list_ids,
        imported_list_titles=imported_list_titles,
        bookmarked_list_ids=bookmarked_list_ids,
        bookmarked_list_titles=bookmarked_list_titles,
    )


# 問題リスト機能
## リスト作成ページ
@main_bp.route("/question", methods=["GET"])
def create_question_get():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login_get"))

    return render_template("question/question.html")


## リスト作成 API
@main_bp.route("/question", methods=["POST"])
def create_question_post():
    form_data = request.form.to_dict()

    # フォームのデータを変換
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

    # 問題リストの内容をデータベースに格納
    creator_id = current_user.id
    list_title = json_data["list_title"]
    question_list = QuestionList(creator_id=creator_id, list_title=list_title)
    db.session.add(question_list)
    db.session.commit()

    # 問題の内容をデータベースに格納
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

        # 問題の選択肢をデータベースに格納
        question_id = question.id
        options_data = question_data["option"]
        for option_text in options_data:
            option = Option(question_id=question_id, option_text=option_text)
            db.session.add(option)
        db.session.commit()

    return redirect(url_for("main.index_get"))


## リスト削除 API
@main_bp.route("/question/delete/<list_id>", methods=["GET"])
def delete_question(list_id):
    question_list = QuestionList.query.filter_by(
        id=list_id, creator_id=current_user.id
    ).first()
    if question_list:
        try:
            BookmarkList.query.filter_by(list_id=question_list.id).delete()
            ImportList.query.filter_by(list_id=question_list.id).delete()
            AnswerResult.query.filter_by(list_id=question_list.id).delete()
            questions = question_list.questions
            for question in questions:
                Option.query.filter_by(question_id=question.id).delete()
            Question.query.filter_by(list_id=question_list.id).delete()
            db.session.delete(question_list)
            db.session.commit()
        except Exception:
            return redirect(url_for("main.index_get"))
    return redirect(url_for("main.index_get"))


# リスト回答機能
## 問題リストの回答ページ
@main_bp.route("/question/<list_id>", methods=["GET"])
def question_content_get(list_id):
    question_list = QuestionList.query.get(list_id)
    if not question_list:
        return render_template("not_found.html")

    # 問題リストの内容を取得
    list_title = question_list.list_title
    creator = User.query.get(question_list.creator_id)
    creator_name = creator.name
    questions = [question.question_text for question in question_list.questions]
    options = []
    for question in question_list.questions:
        question_options = [option.option_text for option in question.options]
        options.append(question_options)

    return render_template(
        "question/question_content.html",
        list_title=list_title,
        creator_name=creator_name,
        questions=questions,
        options=options,
    )


## 問題リストの回答 API
@main_bp.route("/question/<list_id>", methods=["POST"])
def question_content_post(list_id):
    form_data = request.form.to_dict()
    question_list = QuestionList.query.get(list_id)
    if not question_list:
        return render_template("not_found.html")
    correct_answers = [question.correct_answer for question in question_list.questions]

    # ユーザの回答をデータベースに格納
    results = []
    for key, value in form_data.items():
        question_key = int(key[8:])
        answerer_id = current_user.id
        question_id = question_list.questions[question_key - 1].id
        user_answer = int(value)
        answer_result = AnswerResult(
            answerer_id=answerer_id,
            list_id=list_id,
            question_id=question_id,
            user_answer=user_answer,
        )
        db.session.add(answer_result)
        db.session.commit()

        # 正答とユーザの回答を比較
        if correct_answers[question_key - 1] == user_answer:
            results.append(user_answer)
        else:
            results.append(user_answer)

    # 問題リストの内容を取得
    list_title = question_list.list_title
    try:
        answerer_name = User.query.get(answerer_id).name
    except:
        return render_template("not_found.html")
    questions = [question.question_text for question in question_list.questions]
    options = []
    for question in question_list.questions:
        question_options = [option.option_text for option in question.options]
        options.append(question_options)

    return render_template(
        "question/question_result.html",
        list_id=list_id,
        list_title=list_title,
        questions=questions,
        options=options,
        results=results,
        correct_answers=correct_answers,
        answerer_name=answerer_name,
    )


# 回答結果機能
## 回答結果の一覧ページ
@main_bp.route("/question/result/<list_id>", methods=["GET"])
def question_result(list_id):
    return render_template("question/question_result_list.html")


# インポート機能
## 問題リストのインポート API
@main_bp.route("/question/import", methods=["POST"])
def import_question():
    form_data = request.form.to_dict()
    if form_data.get("import") != "":
        try:
            list_id = int(form_data.get("import"))
        except ValueError:
            return redirect(url_for("main.index_get"))
    else:
        return redirect(url_for("main.index_get"))

    question_list = QuestionList.query.get(list_id)
    if question_list is None:
        return redirect(url_for("main.index_get"))

    user_id = current_user.id
    existing_import = ImportList.query.filter_by(
        list_id=list_id, user_id=user_id
    ).first()
    if existing_import is not None:
        return redirect(url_for("main.index_get"))

    import_list = ImportList(list_id=list_id, user_id=user_id)
    db.session.add(import_list)
    db.session.commit()

    return redirect(url_for("main.index_get"))


## インポートの削除 API
@main_bp.route("/question/import/delete/<list_id>", methods=["GET"])
def delete_import(list_id):
    import_list = ImportList.query.filter_by(
        list_id=list_id, user_id=current_user.id
    ).first()
    if import_list:
        try:
            db.session.delete(import_list)
            db.session.commit()
        except Exception:
            return redirect(url_for("main.index_get"))
    return redirect(url_for("main.index_get"))


# ブックマーク機能
## 問題リストのブックマーク API
@main_bp.route("/question/bookmark/<list_id>", methods=["GET"])
def bookmark_question(list_id):
    question_list = QuestionList.query.get(list_id)
    if question_list is None:
        return redirect(url_for("main.index_get"))

    user_id = current_user.id
    existing_bookmark = BookmarkList.query.filter_by(
        list_id=list_id, user_id=user_id
    ).first()
    if existing_bookmark is not None:
        return redirect(url_for("main.index_get"))

    bookmark_list = BookmarkList(list_id=list_id, user_id=user_id)
    db.session.add(bookmark_list)
    db.session.commit()

    return redirect(url_for("main.index_get"))


## ブックマークの削除 API
@main_bp.route("/question/bookmark/delete/<list_id>", methods=["GET"])
def delete_bookmark(list_id):
    bookmark_list = BookmarkList.query.filter_by(
        list_id=list_id, user_id=current_user.id
    ).first()
    if bookmark_list:
        try:
            db.session.delete(bookmark_list)
            db.session.commit()
        except Exception:
            return redirect(url_for("main.index_get"))
    return redirect(url_for("main.index_get"))


# DB リセット機能
@main_bp.route("/reset", methods=["GET"])
def reset():
    db.session.query(ImportList).delete()
    db.session.query(BookmarkList).delete()
    db.session.query(AnswerResult).delete()
    db.session.query(Option).delete()
    db.session.query(Question).delete()
    db.session.query(QuestionList).delete()
    db.session.commit()

    return redirect(url_for("main.index_get"))
