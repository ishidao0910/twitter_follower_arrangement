import json
import requests



def endpoint_user_id_lookup(usernames, user_fields):
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


def endpoint_following_users(user_id, ff, max_results, next_token, user_fields):
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


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200: # HTTPレスポンスステータスコードが200以外ならエラー
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    return response.json()


# get tweet
def get_latest_tweet(oauth, user_number):
    """
    input : user_number 
        ユーザー固有のuser_id
    output : json
        user_idに紐づくユーザーの直近5個のツイート情報(minが5件)
        tweet_idとテキストの中身を選択している
    """
    tweet_number = oauth.get(
        "https://api.twitter.com/2/users/"+str(user_number)+"/tweets?max_results=5&tweet.fields=created_at"
    )
    if tweet_number.status_code != 200 :
        raise Exception(
            "Request returned an error: {}".format(tweet_number)
        )
    # print("Response code: {}".format(tweet_number.status_code), "user_number")
    json_tweet_number = tweet_number.json()
    # print(json.dumps(json_tweet_number, indent=4, sort_keys=True))
    return json_tweet_number
