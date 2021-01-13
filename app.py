#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
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

channel_access_token = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
channel_secret = os.environ['YOUR_CHANNEL_SECRET']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="過去一日の切り抜きをそれぞれ朝9時（ホロライブ）と夕方18時（にじさんじ）に10件ずつ送ります！\n-------------\nURLタップでアプリ内ののブラウザに遷移、サムネイルタップでLINEアプリ内のプレイヤーで視聴します\n-------------\nLINEの「設定」より「LINE Labs」、「リンクをSafariで開く」をオンにすると、URLタップ時にSafariまたはYoutubeアプリで視聴できます（iOSのみ）"))

q1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
q2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'
#youtubeAPIに送信するクエリを設定


#クエリに対する検索結果をLINEに送信
def sendYTresult():
    dt = datetime.datetime.now()
    if dt.hour < 3: #JST時間で12:00以降か以前か判定（UTC時間への補正のため+9時間）
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
            line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text=DeResList))
        except LineBotApiError:
           line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text="エラー"))

sendYTresult()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))