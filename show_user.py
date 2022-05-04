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

def create_url(usernames, user_fields):
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
def get_tweet(user_number):
    """
    input : user_number 
        ユーザー固有のuser_id
    output : json
        user_idに紐づくユーザーの直近10個のツイート情報
        tweet_idとテキストの中身を選択している
    """
    tweet_number = oauth.get(
        "https://api.twitter.com/2/users/"+str(user_number)+"/tweets"
    )
    if tweet_number.status_code != 200 :
        raise Exception(
            "Request returned an error: {} {}".format(tweet_number.status_code, engagement.text)
        )
    print("Response code: {}".format(tweet_number.status_code), "user_number")
    # Saving the response as JSON
    json_tweet_number = tweet_number.json()
    # print(json.dumps(json_tweet_number, indent=4, sort_keys=True))
    return json.dumps(json_tweet_number, indent=4, sort_keys=True, ensure_ascii=False)

# This is my user_id
print(get_tweet(1094899950922563585))

def main():
    usernames = ["BacktestL",]
    user_fields = ["id", "name", "username", "created_at","protected", 
    "withheld", "location", "url", "description", "verified", "entities",
    "profile_image_url", "public_metrics", "pinned_tweet_id"]

    # データ取得
    url = create_url(usernames, user_fields)
    print(url)
    headers = create_headers(bearer_token)
    print(headers)
    json_response = connect_to_endpoint(url, headers)
    print(json_response)
    data =  json_response["data"]
    print(data)



if __name__ == "__main__":
    main()