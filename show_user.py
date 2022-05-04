import configparser
import json
import requests
from requests_oauthlib import OAuth1Session


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

def url_user_id_lookup(usernames, user_fields):
    if(any(usernames)):
        formatted_user_names = "usernames=" + ",".join(usernames)
    else:
        formatted_user_names = ""

    if(any(user_fields)):
        formatted_user_fields = "user.fields=" + ",".join(user_fields)
    else:
        formatted_user_fields = "user.fields=id,name,username"

    url = "https://api.twitter.com/2/users/by?{}&{}".format(formatted_user_names, formatted_user_fields)
    return url


def url_following_users(user_id, ff, max_results, next_token, user_fields):
    if(any(user_fields)):
        formatted_user_fields = "user.fields=" + ",".join(user_fields)
    else:
        formatted_user_fields = ""
    if(next_token is not None):
        formatted_next_token = "&pagination_token=" + (next_token)
    else:
        formatted_next_token = ""
    if(max_results > 1000): max_results = 1000 
    #&pagination_token=
    url = "https://api.twitter.com/2/users/{}/{}?max_results={}{}&{}".format(user_id, ff, max_results, formatted_next_token, formatted_user_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# url：APIリクエスト用のURL headers:APIリクエスト用のヘッダー APIリクエスト
def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200: # HTTPレスポンスステータスコードが200以外ならエラー
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    return response.json()


# get tweet
def get_latest_tweet(user_number):
    """
    input : user_number 
        ユーザー固有のuser_id
    output : json
        user_idに紐づくユーザーの直近10個のツイート情報
        tweet_idとテキストの中身を選択している
    """
    tweet_number = oauth.get(
        "https://api.twitter.com/2/users/"+str(user_number)+"/tweets?max_results=5&tweet.fields=created_at"
    )
    if tweet_number.status_code != 200 :
        raise Exception(
            "Request returned an error: {}".format(tweet_number)
        )
    print("Response code: {}".format(tweet_number.status_code), "user_number")
    # Saving the response as JSON
    json_tweet_number = tweet_number.json()
    # print(json.dumps(json_tweet_number, indent=4, sort_keys=True))
    return json_tweet_number
    # return json.dumps(json_tweet_number, indent=4, sort_keys=True, ensure_ascii=False)

def main():
    usernames = ["BacktestL"] #　input

    user_fields = ["id", "name", "username", "public_metrics",]
    url = url_user_id_lookup(usernames, user_fields)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    user_id =  json_response["data"][0]['id']

    ff = "following"    
    max_results = 5 # 取得したいデータ数
    user_fields = ["id", "name", "username","description",]
    
    #### データ取得
    following_users_id = []
    next_token = None
    data_len = 0
    while(True):
        url = url_following_users(user_id, ff, max_results, next_token, user_fields)
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
        following_users_id.append(data_ele['id'])


    # print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    print(following_users_id)
    for following_user_id in following_users_id:
        data = get_latest_tweet(following_user_id)
        latest_tweet_created = data['data'][0]['created_at']
        latest_tweet = data['data'][0]['text']
        print(latest_tweet_created, ":", latest_tweet)


if __name__ == "__main__":
    main()