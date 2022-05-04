import configparser
import json
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

# get tweet
def tweet_input(user_number):
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
print(tweet_input(1094899950922563585))