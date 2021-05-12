# vtuber-notification
○作ろうとした背景  
・バーチャルyoutuberが好き  
・日常的に、色んなvtuberの配信切り抜き動画を色んなチャンネルが投稿している。  
・「あなたへのおすすめ」やチャンネル登録では追いつかない。  
・数ヶ月前のバズってた切り抜き動画（知らない話題）を知る→その時見れなかった歯がゆさ  

○通知媒体  
・LINEbot

○利用したもの  
・line messaging api  
・youtube api  
・flask  
・heroku  

○仕組み  
lineで調べたいワード送信  
→  
linebotサーバー  
→  
herokuサーバー  
→  
「検索ワード：送信されたワード,再生数順,過去一日以内に投稿された動画,最大5件」の条件でyoutubeAPIにリクエスト  
→  
heroku・linebotを経由してLINEに検索結果を5件表示  

○QRコード  

![206sqinn](https://user-images.githubusercontent.com/62412012/117532281-9bd88600-b021-11eb-83de-e27d5c1e45b7.png)
