#!/usr/bin/python
# -*- coding: utf-8 -*-
from apiclient import discovery
from time import time
import datetime


class ytResponse:
    def ytResponse(self,query):
        YOUTUBE_API_KEY = 'AIzaSyCx0b1EJjx4h70TfkJ4L6El9htNHGEx1j0'
        youtube = discovery.build('youtube', 'v3' ,developerKey=YOUTUBE_API_KEY)

        unixnowtime=time()
        #現在のunixタイムを格納
        unix1dayago=int(unixnowtime)-118800
        #一日前のunixタイムを格納
        RFC3339_1dp=datetime.datetime.fromtimestamp(unix1dayago)
        #unixタイムをRFC3339方式に変更
        ztime=RFC3339_1dp.isoformat("T")+"Z"
        #RFC3339方式にZ（グリニッジ標準時）を入れ込む

        search_response = youtube.search().list(
          part='snippet',
          publishedAfter=ztime,#昨日以降に投稿された動画を指定
          q=query,
          maxResults=5,
          order='viewCount',
          type='video',
          ).execute()
        #youtubeAPIを使用し検索結果を条件付きで絞る


        dic={}

        for sr in search_response.get("items", []):
            dic[sr['snippet']['title']] = 'https://www.youtube.com/watch?v='+sr['id']['videoId']

        return dic
        #取得した動画のタイトルとurlの辞書リスト
