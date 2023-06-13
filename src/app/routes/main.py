from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

# ホームページ API
@main_bp.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")