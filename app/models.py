from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user
from flask import redirect
from app import db, admin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    isAdmin = Column(Boolean, default=False)

    def __str__(self):
        return self.name

class Team(db.Model):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    homestadium = Column(String(50), nullable=False)
    image = Column(String(100))
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
    position = Column(String(50), nullable=False)
    height = Column(String(50), nullable=False)
    weight = Column(String(50), nullable=False)
    image = Column(String(100))
    note = Column(String(100))
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

    def __str__(self):
        return str(self.id)


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

    def __str__(self):
        return self.name


class TypeOfScore(db.Model):
    __tablename__ = "typeofscore"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    scores = relationship('Score', backref='Type of score', lazy=True)

    def __str__(self):
        return self.name


class Round(db.Model):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    matches = relationship('Match', backref='round', lazy=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    regular_price = Column(DECIMAL, nullable=False)

    def __str__(self):
        return self.name


class Cart(db.Model):
    __tablename__ = "cart"
    userid = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    productid = Column(Integer, ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity = Column(Integer, nullable=False)

    def __str__(self):
        return self.name

class Order(db.Model):
        __tablename__ = "order"
        id = Column(Integer, primary_key=True, autoincrement=True)
        order_date = Column(DateTime, nullable=False)
        total_price = Column(DECIMAL, nullable=False)
        userid = db.Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)

        def __str__(self):
            return self.name


class OrderedProduct(db.Model):
    __tablename__ = "order_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer, ForeignKey('order.id'), nullable=False)
    productid = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


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
admin.add_view(AuthenticatedView(Product, db.session))
admin.add_view(AuthenticatedView(Cart, db.session))
admin.add_view(AuthenticatedView(Order, db.session))
admin.add_view(AuthenticatedView(OrderedProduct, db.session))
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogOutView(name="Log out"))

if __name__ == "__main__":
    db.create_all()
