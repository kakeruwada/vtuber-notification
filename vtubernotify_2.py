#!/usr/bin/python
# -*- coding: utf-8 -*-
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import ytResponse
import pprint
from flask import Flask, jsonify, abort

channel_access_token = ('gdwFD3CEbW2keHoILCal0xC9nTEy4PdLfLEmqnai2w8N1x8Gcy24EhAfSFh7m8MMesD1/d7e+OmblqrazFVQiLbEwE55eBYcy64QW9n52CkfyUX4NFsl4t6AC4kRz4IEOdosSS/pAQtCI4Kq14rAHgdB04t89/1O/w1cDnyilFU=')

line_bot_api = LineBotApi(channel_access_token)

app = Flask(__name__)

@app.route('/callback')
def callback():
    return abort(200)

q1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
q2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'

#qlist = [q1]
#qlist.extend([q2, q1])
Response = ytResponse.ytResponse().ytResponse(q1)
listedRes = list(Response.items())
#クエリを指定して検索結果を取得

#検索結果を1動画ずつ出力（LINEメッセージにて見やすくするため）
for R in range(len(listedRes)):
    item = listedRes[R]
    pResList = pprint.pformat(item)
    #辞書形式からリストに変更しpprintで見やすくする
    DeResList = str(pResList).decode('string-escape')
    #デコード処理
    try:
        line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text=DeResList))
    except LineBotApiError:
        line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text="エラー"))
