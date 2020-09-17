from app import app
import secrets
import json
import os
import urllib.request
import urllib.response
import uuid
import hmac
import hashlib
from app.models import Team, Player, User, Rule, Score


def read_team():
    return Team.query.all()


def read_player():
    return Player.query.all()

def read_user():
    return User.query.all()

def read_rule():
    return Rule.query.all()

def total_score_by_players():
    players = (Player.query.all())
    player_and_score = []
    for player in players:
        score = Score.query
        score = score.filter(Score.player_id == player.id)
        totalScore = len(score.all())
        player_name = get_player_by_player_id(player.id).name
        player_type = get_player_by_player_id(player.id).type
        team_name = get_name_by_team_id(get_player_by_player_id(player.id).team_id)
        temp = [player_name, team_name, player_type, totalScore]
        player_and_score.append(temp)
    return player_and_score

def get_player_by_player_id(player_id):
    player = Player.query
    player = player.filter(Player.id == player_id)
    return player.all()[0]

def get_name_by_team_id(team_id):
    team = Team.query
    team = team.filter(Team.id == team_id)
    return team.all()[0]

def payment_momo():
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOY1ZA20200907"
    accessKey = "rVuWIV2U6YHmb803"
    serectkey = "EQeEkD4sirbclirmqPv5qXDrcLu2h5EZ"
    orderInfo = "pay with MoMo"
    returnUrl = "https://momo.vn/return"
    notifyurl = "https://dummy.url/notify"
    amount = "2000000"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureMoMoWallet"
    extraData = "merchantName=;merchantId="

    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData


    h = hmac.new(serectkey.encode('utf-8'), rawSignature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()




    data = {
        'partnerCode': partnerCode,
        'accessKey': accessKey,
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'returnUrl': returnUrl,
        'notifyUrl': notifyurl,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }

    data = json.dumps(data)

    clen = len(data)
    req = urllib.request.Request(
        endpoint,
        data.encode('utf-8'),
        {'Content-Type': 'application/json', 'Content-Length': clen}
    )
    f = urllib.request.urlopen(req)

    response = f.read()
    f.close()

    return json.loads(response)
