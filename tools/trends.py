import feedparser
import requests

def reddit_trends():
    url = "https://www.reddit.com/r/technology/hot.json?limit=10"
    headers = {"User-Agent": "agent"}

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        return [p["data"]["title"] for p in data["data"]["children"]]
    except:
        return []

def hackernews_trends():
    url = "https://hnrss.org/frontpage"
    feed = feedparser.parse(url)

    return [entry.title for entry in feed.entries[:10]]

def get_trends(keywords):
    reddit = reddit_trends()
    hn = hackernews_trends()

    combined = reddit + hn
    return combined[:10]