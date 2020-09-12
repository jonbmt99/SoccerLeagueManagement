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

# @app.route("/search-player", methods=['post', 'get'])
# def SearchPlayer():
#     data_form = request.form['position']
#     print(data_form)
#     return "ádsa"

@app.route("/ticket")
def tickets():
    return render_template("ticket.html")

@app.route("/player")
def players():
    kw = request.args.get("keyword")
    position = request.args.get("position")
    return render_template("player.html", playerList=dao.read_player(keyword=kw, position=position))

@app.route("/team-detail")
def team_details():
    team_id = request.args.get("teamId")
    # team_test = dao.read_team_by_id(team_id)
    # print(team_test)
    return render_template("teamDetail.html", team=dao.read_team_by_id(team_id))

@app.route("/matches")
def matches():
    return render_template("match.html")

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
