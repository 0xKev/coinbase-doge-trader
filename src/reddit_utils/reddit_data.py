import praw
import os
from dotenv import load_dotenv

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

class RedditClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="python:dog-stats:v0.1.0 (by /u/crunchy)"
        )

    def get_titles(self) -> list[str]:
        titles = []
        for submission in self.client.subreddit("aww").top(time_filter="day", limit=5):
            titles.append(submission.title)
        return titles
    
if __name__ == "__main__":


    reddit = RedditClient(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
    )
    print(reddit.get_titles())

    
    
    
