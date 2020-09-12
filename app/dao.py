from app import app
import secrets
import json
import os
import urllib.request
import urllib.response
import uuid
import hmac
import hashlib
from app.models import Team, Player, User


def read_team():
    return Team.query.all()


def read_player():
    return Player.query.all()


def read_user():
    return User.query.all()


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