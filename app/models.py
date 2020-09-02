from sqlalchemy import Column, Integer, String, DateTime, Boolean,  ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user
from flask import redirect
from app import db, admin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

class Team(db.Model):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    players = relationship('Player', backref='team', lazy=True)
    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    national = Column(String(50), nullable=False)
    dayofbirth = Column(DateTime, nullable=False)
    type = Column(String(50), nullable=False)
    note = Column(String(100), nullable=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)

    def __str__(self):
        return self.name

class Match(db.Model):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hometeam_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    awayteam_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    hometeam = relationship("Team", foreign_keys=[hometeam_id])
    awayteam = relationship("Team", foreign_keys=[awayteam_id])
    matchtime = Column(DateTime, nullable=False)
    stadium = Column(String(50), nullable=False)
    result = Column(String(10), nullable=False)
    round_id = Column(Integer, ForeignKey('round.id'), nullable=False)

class Score(db.Model):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('match.id'), nullable=False)
    match = relationship("Match", foreign_keys=[match_id])
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    team = relationship("Team", foreign_keys=[team_id])
    player = relationship("Player", foreign_keys=[player_id])
    type_of_score_id = Column(Integer, ForeignKey('typeofscore.id'), nullable=False)

class TypeOfScore(db.Model):
    __tablename__ = "typeofscore"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    scores = relationship('Score', backref='Type of score', lazy=True)

class Round(db.Model):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=False)
    matches = relationship('Match', backref='round', lazy=True)

class Rule(db.Model):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    min_players = Column(Integer, nullable=False)
    max_players = Column(Integer, nullable=False)
    max_foreign_players = Column(Integer, nullable=False)
    max_time_score = Column(Integer, nullable=False)
    win_point = Column(Integer, nullable=False)
    draw_point = Column(Integer, nullable=False)
    lose_point = Column(Integer, nullable=False)

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")

    def is_accessible(self):
        return current_user.is_authenticated

class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(AuthenticatedView(Team, db.session))
admin.add_view(AuthenticatedView(Player, db.session))
admin.add_view(AuthenticatedView(Match, db.session))
admin.add_view(AuthenticatedView(Score, db.session))
admin.add_view(AuthenticatedView(TypeOfScore, db.session))
admin.add_view(AuthenticatedView(Round, db.session))
admin.add_view(AuthenticatedView(Rule, db.session))
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogOutView(name="Log out"))

if __name__ == "__main__":
    db.create_all()

