import configparser
from requests_oauthlib import OAuth1Session
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

usernames = ["BacktestL"] #　input

user_fields = ["id", "name", "username", "public_metrics",]
url = endpoint_user_id_lookup(usernames, user_fields)
headers = create_headers(bearer_token)
json_response = connect_to_endpoint(url, headers)
user_id =  json_response["data"][0]['id']

print("user_id ", user_id)

ff = "following"    
max_results = 5 # 取得したいデータ数
user_fields = ["id", "name", "username","description",]

#### データ取得
following_users_id = []
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

print(data)