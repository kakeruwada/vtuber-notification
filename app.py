#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import psycopg2
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
import psycopg2
from psycopg2.extras import DictCursor

#--環境変数系

app = Flask(__name__)

channel_access_token = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
channel_secret = os.environ['YOUR_CHANNEL_SECRET']
database_url = os.environ.get('DATABASE_URL')

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#--データベース系の関数

def get_response_message(num,line_mess):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            sql = "CREATE TABLE IF NOT EXISTS query_table (id int,name text, UNIQUE (id))"
            sql_isert = "INSERT INTO query_table(id, name) VALUES('{}', '{}') ON CONFLICT (id) DO UPDATE SET name = '{}'".format(str(num), line_mess, line_mess)

            cur.execute(sql)#if not条件付きでテーブルを作る

            cur.execute(sql_isert)#指定した条件をテーブルに登録

#--LINEメッセージ系


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_mssg = event.message.text
    if  "登録1" in line_mssg:
        splt = line_mssg.split(":")
        srch_wrd = splt[1]

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= srch_wrd + "を登録したよ！"))


        get_response_message(1,srch_wrd)


    elif "登録2" in line_mssg:
        splt = line_mssg.split(":")
        srch_wrd = splt[1]

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= srch_wrd + "を登録したよ！"))

        get_response_message(2,srch_wrd)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="にゃーん"))


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
        TextSendMessage(text="過去一日の動画をそれぞれ朝8時と朝10時に10件ずつ送ります！\n-------------\nURLタップでアプリ内ののブラウザに遷移、サムネイルタップでLINEアプリ内のプレイヤーで視聴します\n-------------\nLINEの「設定」より「LINE Labs」、「リンクをSafariで開く」をオンにすると、URLタップ時にSafariまたはYoutubeアプリで視聴できます（iOSのみ）\n-------------\n検索ワードに設定したいワードは「登録:〇〇（任意のワード）」のフォーマットで登録:は半角　"))



    #クエリに対する検索結果をLINEに送信
def send_yt_result():
    with psycopg2.connect(database_url) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            q1 = cur.execute("SELECT name FROM query_table WHERE id = 1")
            q2 = cur.execute("SELECT name FROM query_table WHERE id = 2")
            dt = datetime.datetime.now()
            if dt.hour < 12 and q1 != []:
                Response = ytResponse.ytResponse().ytResponse(q1)
                #JST時間で9:00~21:00はq2の検索結果
            elif q2 != []:
                Response = ytResponse.ytResponse().ytResponse(q2)
                #JST時間で21:00~9:00はq2の検索結果
            else:
                sys.exit()

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