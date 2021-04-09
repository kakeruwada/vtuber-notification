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
from flask import Flask, request, abort

import ytResponse
import pprint
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

query1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
query2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'

class application():

    #LINEAPIからのHTTPリクエストの署名を検証し、問題ない場合任意の関数を実行
    @app.route("/callback", methods=['POST'])
    def callback(self):
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
    def handle_follow(self, event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="過去一日の切り抜きをそれぞれ朝8時（にじさんじ）と朝10時（ホロライブ）に10件ずつ送ります！\n-------------\nURLタップでアプリ内ののブラウザに遷移、サムネイルタップでLINEアプリ内のプレイヤーで視聴します\n-------------\nLINEの「設定」より「LINE Labs」、「リンクをSafariで開く」をオンにすると、URLタップ時にSafariまたはYoutubeアプリで視聴できます（iOSのみ）"))

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

    #クエリに対する検索結果をLINEに送信
    def send_yt_result(q1,q2):
        dt = datetime.datetime.now()
        if dt.hour < 12:
            Response = ytResponse.ytResponse().ytResponse(q1)
            #JST時間で9:00~21:00はq2の検索結果
        else:
            Response = ytResponse.ytResponse().ytResponse(q2)
            #JST時間で21:00~9:00はq2の検索結果

        listed_res = list(Response.items())
        #クエリを指定して検索結果を取得

        #検索結果を1動画ずつ出力（LINEメッセージにて見やすくするため）
        for r in range(len(listed_res)):
            item = listed_res[r]
            pp_response = pprint.pformat(item)
            #辞書形式からリストに変更しpprintで見やすくする
            try:
                line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text=pp_response))
            except LineBotApiError:
                line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text="エラーが発生しました"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))