#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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

# Herokuの変数からトークンなどを取得
channel_secret = ('2c9ceaf2583460f2a84b472daab233fa')
channel_access_token = ('gdwFD3CEbW2keHoILCal0xC9nTEy4PdLfLEmqnai2w8N1x8Gcy24EhAfSFh7m8MMesD1/d7e+OmblqrazFVQiLbEwE55eBYcy64QW9n52CkfyUX4NFsl4t6AC4kRz4IEOdosSS/pAQtCI4Kq14rAHgdB04t89/1O/w1cDnyilFU=')

line_bot_api = LineBotApi(channel_access_token)

q1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
q2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'

qlist = []
qlist.extend([q2, q1])

for q in qlist:
    Res = ytResponse.ytResponse()
    r = Res.ytResponse(q)
    ResList = list(r.items())
    pResList = pprint.pformat(ResList)
    DeResList = str(pResList).decode('string-escape')
    try:
        line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text=DeResList))
    except LineBotApiError:
        line_bot_api.push_message('Uf0f5062854847968101f84a27657f739', TextSendMessage(text="エラー"))
