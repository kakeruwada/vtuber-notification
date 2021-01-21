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
        TextSendMessage(text="過去一日の切り抜きをそれぞれ朝8時（にじさんじ）と朝10時（ホロライブ）に10件ずつ送ります！\n-------------\nURLタップでアプリ内ののブラウザに遷移、サムネイルタップでLINEアプリ内のプレイヤーで視聴します\n-------------\nLINEの「設定」より「LINE Labs」、「リンクをSafariで開く」をオンにすると、URLタップ時にSafariまたはYoutubeアプリで視聴できます（iOSのみ）"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))