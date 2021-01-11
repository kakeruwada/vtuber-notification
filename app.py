#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage,
)
import ytResponse
import pprint
from flask import Flask, request, abort
import datetime

app = Flask(__name__)

channel_access_token = ('gdwFD3CEbW2keHoILCal0xC9nTEy4PdLfLEmqnai2w8N1x8Gcy24EhAfSFh7m8MMesD1/d7e+OmblqrazFVQiLbEwE55eBYcy64QW9n52CkfyUX4NFsl4t6AC4kRz4IEOdosSS/pAQtCI4Kq14rAHgdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler('2c9ceaf2583460f2a84b472daab233fa')

#LINEAPIからのHTTPリクエストの署名を検証し、問題ない場合任意の関数を実行
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#LINEアカウントがフォローされた時にメッセージを送信
@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="過去一日の切り抜きをそれぞれ朝9時（ホロライブ）と夕方18時（にじさんじ）に10件ずつ送ります！\n-------------\nURLタップでアプリ内ののブラウザに遷移、サムネイルタップでLINEアプリ内のプレイヤーで視聴します\n-------------\nLINEの「設定」より「LINE Labs」、「リンクをSafariで開く」をオンにすると、URLタップ時にSafariまたはYoutubeアプリで視聴できます（iOSのみ）"))

q1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
q2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'
#youtubeAPIに送信するクエリを設定

#クエリに対する検索結果をLINEに送信
def sendYTresult():
    dt = datetime.datetime.now()
    if dt.hour < 12:
        Response = ytResponse.ytResponse().ytResponse(q1)
    else:
        Response = ytResponse.ytResponse().ytResponse(q2)
    #午前はホロライブ、午後はにじさんじの切り抜きを通知

    listedRes = list(Response.items())
    #クエリを指定して検索結果を取得

    #検索結果を1動画ずつ出力（LINEメッセージにて見やすくするため）
    for R in range(len(listedRes)):
        item = listedRes[R]
        pResList = pprint.pformat(item)
        #辞書形式からリストに変更しpprintで見やすくする
        DeResList = pResList
        #デコード処理
        try:
            line_bot_api.push_message(profile.user_id, TextSendMessage(text=DeResList))
        except LineBotApiError:
           line_bot_api.push_message(profile.user_id, TextSendMessage(text="エラー"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))