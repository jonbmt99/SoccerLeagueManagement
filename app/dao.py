from app import app
import json
import os
import hashlib
from app.models import Team, Player

def read_team():
    return Team.query.all()

def read_player(keyword=None, position=None):
    p = Player.query

    if keyword:
        p = p.filter(Player.name.contains(keyword))
    if position:
        p = p.filter(Player.position.contains(position))
    return p.all()

def read_team_by_id(id:int):
    return Team.query.get(id)

