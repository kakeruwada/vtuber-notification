
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

import ytapi
import pprint
import datetime


#--環境変数系--



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

#--LINEメッセージ系

#メッセージを貰った時に、動画検索結果をリプライ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_mssg = event.message.text
    if  type(line_mssg) == str : #メッセージがstr型だった場合、

        Res = ytapi.ytres()
        response = Res.ytResponse(line_mssg)

        listed_res = list(response.items())
        #クエリを指定して検索結果を取得

        #検索結果を1動画ずつ出力（LINEメッセージにて見やすくするため）
        for r in listed_res:
            item = r[1] + "\n" + r[2]

            try:
                line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text=item))
            except LineBotApiError:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= "エラーが発生しました" ))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好きなワードを送ってね"))


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
        TextSendMessage(text="自分の好きなキーワードを送信してみてね！\n↓\nそのキーワードで過去一日以内に投稿された動画のうち再生数TOP5の動画が送られてくるよ！\n※時間を置くと動画送信に時間がかかる場合があるよ！\n\n【Tip】\nIOSの人は「設定」→「LINE Labs」→「リンクをデフォルトのブラウザで開く」をONにすると、送信された動画リンクタップでyoutubeアプリで視聴できるよ！"))

#----LINEメッセージ系終了


#----使用しない関数（send_yt_result）
    #クエリに対する検索結果を定期的にLINEに送信

def send_yt_result(q1, q2):
    dt = datetime.datetime.now()

    if dt.hour < 12:
        Res = ytapi.ytres().ytResponse()
        query = q1
        #JST時間で9:00~21:00はq2の検索結果
    else:
        Res = ytapi.ytres().ytResponse()
        query = q2
        #JST時間で21:00~9:00はq2の検索結果
    response = Res.ytResponse(query)
    listed_res = list(response.items())
    #クエリを指定して検索結果を取得

    #検索結果を1動画ずつ出力（LINEメッセージにて見やすくするため）
    for r in listed_res:
        item = r[1] + "\n" + r[2]

        try:
            line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text=item))
        except LineBotApiError:
            line_bot_api.push_message("Uf0f5062854847968101f84a27657f739", TextSendMessage(text="エラーが発生しました"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))