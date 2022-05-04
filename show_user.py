import configparser
from requests_oauthlib import OAuth1Session


config_ini = configparser.ConfigParser(interpolation=None)
config_ini.read('config.ini', encoding='utf-8')
print(config_ini)

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

print(oauth)