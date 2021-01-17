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
import datetime

channel_access_token = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)

query1 = 'ホロライブ切り抜き　OR　ホロライブ手描き'
query2 = 'にじさんじ切り抜き OR にじさんじ手描き OR にじさんじ漫画'
#youtubeAPIに送信するクエリを設定

#クエリに対する検索結果をLINEに送信
def send_yt_result(q1,q2):
    dt = datetime.datetime.now()
    if dt.hour < 15: #JST時間で9:00以降か以前か判定（UTC時間への補正のため+9時間）
        Response = ytResponse.ytResponse().ytResponse(q1)
    else:
        Response = ytResponse.ytResponse().ytResponse(q2)
    #午前はホロライブ、午後はにじさんじの切り抜きを通知
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
    send_yt_result(query1,query2)