from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user


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

    for key, value in form_data.items():
        if key.startswith("question"):
            print(form_data)
    return jsonify(form_data)