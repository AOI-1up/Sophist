import os
from os.path import join, dirname
from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

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

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define DB tables
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


# Home Page
@app.route("/",methods=['GET'])
def index_get():
    return render_template('index.html')


# UserList Page
@app.route("/users",methods=['GET'])
def users_get():
    users = User.query.all()
    return render_template('users_get.html', users=users)


# User Add Process
@app.route("/users",methods=['POST'])
def users_post():
    user = User(
        name=request.form["user_name"]
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users_get'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)