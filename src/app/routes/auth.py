from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# ユーザー登録用 API
@auth_bp.route('/register', methods=['GET'])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for('main.index_get'))
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register_post():
    user = User(
        name=request.form["user_name"],
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('auth.login_get'))

# ユーザーログイン用 API
@auth_bp.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('main.index_get'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()
    if user is None or not user.check_password(request.form["password"]):
        flash('メールアドレスかパスワードが間違っています')
        return redirect(url_for('auth.login_get'))
    login_user(user)
    return redirect(url_for('main.index_get'))

# ユーザーログアウト用 API
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index_get'))