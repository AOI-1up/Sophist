from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('main.index_get'))

    return render_template('login.html')