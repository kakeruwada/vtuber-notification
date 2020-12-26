#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, abort
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

app = Flask(__name__)

# Herokuの変数からトークンなどを取得
channel_secret = os.environ['fbb542ba66625af9a766812a2ab62d18']
channel_access_token = os.environ['gdwFD3CEbW2keHoILCal0xC9nTEy4PdLfLEmqnai2w8N1x8Gcy24EhAfSFh7m8MMesD1/d7e+OmblqrazFVQiLbEwE55eBYcy64QW9n52CkfyUX4NFsl4t6AC4kRz4IEOdosSS/pAQtCI4Kq14rAHgdB04t89/1O/w1cDnyilFU=']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# LINEからのWebhook
@app.route("/callback", methods = ['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

q1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
Res = ytResponse.ytResponse()
r = Res.ytResponse(q1)
#utf_8にエンコードが必要
pfmtlist=pprint.pformat(list(r.values()))
pfmtlist_encoded=pfmtlist.encode('utf_8')

try:
    line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text=pfmtlist))
except LineBotApiError:
    line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text="エラー"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT"))
