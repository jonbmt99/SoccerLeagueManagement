from flask import render_template, request
from flask_login import login_user
from app import app, login, dao
from app.models import *
import hashlib
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/team")
def teams():
    return render_template("team.html", teamList=dao.read_team())

@app.route("/player")
def players():
    return render_template("player.html", playerList=dao.read_player())

@app.route("/login-admin", methods = ['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
