# twitter_follower_arrangement
自分のフォローしている人の最新のツイートと投稿日を取得して、ここ数年活動していない人などを整理できる

# UI

## form
<img width="668" alt="スクリーンショット 2022-05-05 7 27 12" src="https://user-images.githubusercontent.com/73809994/166835705-73e4efab-c528-498d-ba46-03177f1664a1.png">

## result
<img width="1118" alt="スクリーンショット 2022-05-15 0 50 25" src="https://user-images.githubusercontent.com/73809994/168439224-f4b8dbb6-f649-409e-98d5-83ea931143d7.png">


# terminal
<img width="803" alt="スクリーンショット 2022-05-05 7 27 26" src="https://user-images.githubusercontent.com/73809994/166835726-111b1011-8aa1-44ce-b348-61a1df09c475.png">

# docker操作

ビルドする
```
docker build -t follower_arrangement .
```

コンテナ立ち上げる
```
docker container run -it -p 8000:5000 -v {{作業ディレクトリ}}/src:/workdir --name follower_arrangement follower_arrangement /bin/bash
```

コンテナ起動
```
docker start follower_arrangement
```

コンテナに入る
```
docker exec -it follower_arrangement bash
```

