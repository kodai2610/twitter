import tweepy
import json
from requests_oauthlib import OAuth1Session
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
MY_SHINJYUKU_COLLECTION_ID = os.getenv("MY_SHINJYUKU_COLLECTION_ID")

# 認証
tweepy_auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
tweepy_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = OAuth1Session(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(tweepy_auth)


def main():
    with open("idlist_shinjyuku.txt", "r") as f:
        tweet_ids = list(map(lambda s: int(s), f.read().splitlines()))
    # tweet_ids = get_tweets("新宿 from:meteorite_0825")
    tweet_ids.sort()
    res = add_collection(tweet_ids, MY_SHINJYUKU_COLLECTION_ID)
    print(res)


# 取得したツイートを配列に格納する関数
def get_tweets(query):
    tweet_ids = []
    tweets = tweepy_api.search_full_archive(
        label="full", query=query, fromDate="200701012315"
    )
    with open("idlist_shinjyuku.txt", "w") as f:
        for tweet in tweets:
            tweet_ids.append(tweet.id)
            print(tweet.id, file=f)

    return tweet_ids


# ツイートをコレクションに追加する関数
def add_collection(tweet_ids, collection_id):
    url = "https://api.twitter.com/1.1/collections/entries/add.json"

    for tweet_id in tweet_ids:
        params = {
            "id": collection_id,
            "tweet_id": tweet_id,
        }
        res = api.post(url, params=params)
        time.sleep(3)

    return res.json()


if __name__ == "__main__":
    main()
