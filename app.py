import configparser
from tkinter.tix import TixWidget
from requests_oauthlib import OAuth1Session
from flask import Flask,render_template, request
from twitter_api.users_api import endpoint_user_id_lookup
from twitter_api.users_api import endpoint_following_users
from twitter_api.users_api import create_headers
from twitter_api.users_api import connect_to_endpoint
from twitter_api.users_api import get_latest_tweet


config_ini = configparser.ConfigParser(interpolation=None)
config_ini.read('config.ini', encoding='utf-8')

# 取得した各種キーを格納-----------------------------------------------------
consumer_key=config_ini['DEFAULT']['API_KEY']
consumer_secret=config_ini['DEFAULT']['API_SECRET_KEY']
access_token=config_ini['DEFAULT']['ACCESS_TOKEN']
access_token_secret=config_ini['DEFAULT']['ACCESS_TOKEN_SECRET']
bearer_token = config_ini['DEFAULT']['BEARER_TOKEN']

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

#flaskオブジェクトの作成
app = Flask(__name__)

#htmlファイルの値を受け取る
@app.route('/', methods=['GET'])
def get():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def post():
    twitter_id = [request.form['twitter_id']]

    user_fields = ["id", "name", "username", "public_metrics",]
    url = endpoint_user_id_lookup(twitter_id, user_fields)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    user_id =  json_response["data"][0]['id']
    # print("user id ", user_id)

    ff = "following"    
    max_results = 25 # 取得したいデータ数
    user_fields = ["id", "name", "username","description",]

    following_users_id = []
    following_user_name = []
    next_token = None
    data_len = 0
    while(True):
        url = endpoint_following_users(user_id, ff, max_results, next_token, user_fields)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        data = json_response["data"]
        meta = json_response["meta"]

        #### 終了チェック(欲しい数に達するか全て取り終わったら終了)
        data_len += len(data)
        if(max_results <= data_len): break
        if(not "next_token" in meta): break
        next_token = meta["next_token"]
    pass
    for data_ele in data:
        following_user_name.append(data_ele['username'])
        following_users_id.append(data_ele['id'])

    # print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    # print(following_users_id)
    name_list = []
    last_tweet_created_list = []
    latest_tweet_list = []
    for name, following_user_id in zip(following_user_name, following_users_id):
        data = get_latest_tweet(oauth, following_user_id)
        latest_tweet_created = data['data'][0]['created_at']
        latest_tweet = data['data'][0]['text']
        name_list.append(name)
        last_tweet_created_list.append(latest_tweet_created)
        latest_tweet_list.append(latest_tweet)

    # print(name_list)
    # print(last_tweet_created_list)
    # print(latest_tweet_list)
    return render_template('result.html', 
    name=name_list, 
    last_tweet_created=last_tweet_created_list, 
    latest_tweet=latest_tweet_list
    )

#pythonで実行されたときに処理をする
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)