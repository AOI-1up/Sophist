import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


# SQLAlchrmy Settings
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv()
DB_USER = os.environ['MYSQL_USER']
DB_PASS = os.environ['MYSQL_PASSWORD']
DB_HOST = "db"
DB_NAME = os.environ['MYSQL_DATABASE']

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


# Define DB tables
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Home Page
@app.route("/",methods=['GET'])
def index_get():
    return render_template('index.html')


# Register User
@app.route("/register",methods=['GET'])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for('index_get'))

    return render_template('register.html')

@app.route("/register",methods=['POST'])
def users_post():
    user = User(
        name=request.form["user_name"],
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login_get'))


# Login User
@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('index_get'))

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()

    if user is None or not user.check_password(request.form["password"]):
        flash('メールアドレスかパスワードが間違っています')
        return redirect(url_for('login_get'))

    login_user(user)
    return redirect(url_for('index_get'))


# Logout User
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index_get'))


# Delete User
@app.route("/users/<id>/delete",methods=['POST'])
def users_id_post_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_get'))


# UserList Page
@app.route("/users",methods=['GET'])
def users_get():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    users = User.query.all()
    return render_template('users_get.html', users=users)


# User Page
@app.route("/users/<id>",methods=['GET'])
def users_id_get(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    if str(current_user.id) != str(id):
        return Response(response="Forbidden", status=403)
    user = User.query.get(id)
    return render_template('users_id_get.html', user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)