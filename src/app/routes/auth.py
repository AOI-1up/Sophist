from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__)


# ユーザー登録ページ
@auth_bp.route("/register", methods=["GET"])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for("main.index_get"))

    return render_template("auth/register.html")


# ユーザー登録 API
@auth_bp.route("/register", methods=["POST"])
def register_post():
    user_name = request.form.get("user_name")
    mail = request.form.get("mail")
    password = request.form.get("password")

    if not user_name or not mail or not password:
        flash("全てのフィールドを入力してください")
        return redirect(url_for("auth.register_get"))

    try:
        user = User(name=user_name, mail=mail)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        flash("このメールアドレスは既に登録されています。")
        return redirect(url_for("auth.register_get"))

    return redirect(url_for("auth.login_get"))


# ログインページ
@auth_bp.route("/login", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for("main.index_get"))

    return render_template("auth/login.html")


# ログイン API
@auth_bp.route("/login", methods=["POST"])
def login_post():
    mail = request.form.get("mail")
    password = request.form.get("password")

    if not mail or not password:
        flash("メールアドレスとパスワードを入力してください")
        return redirect(url_for("auth.login_get"))

    user = User.query.filter_by(mail=mail).one_or_none()
    if user is None or not user.check_password(password):
        flash("メールアドレスかパスワードが間違っています")
        return redirect(url_for("auth.login_get"))

    login_user(user)
    return redirect(url_for("main.index_get"))


# ログアウト API
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index_get"))
