from app import app
import json
import os
import hashlib
from app.models import Team, Player

def read_team():
    return Team.query.all()

def read_player():
    return Player.query.all()