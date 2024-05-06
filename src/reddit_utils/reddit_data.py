import praw
import os
from dotenv import load_dotenv
import string

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
        self.cat_word_lists = {
            'doggo', 'pupper', 'good boy', 'good girl', 'bork', 'woof', 'puppy eyes',
            'snoot', 'belly rub', 'ear scratch', 'head tilt', 'tippy taps', 'wigglebutt',
            'doggo language', 'puppy tax', 'dog tax', 'rescue dog', 'mutt', 'purebred',
            'dog park', 'puppy kindergarten', 'dog training', 'positive reinforcement',
            'treat', 'boop the snoot', "who's a good boy", "who's a good girl"
        }
        self.dog_word_lists = {
            'catto', 'kitty', 'kitten', 'purr', 'meow', 'beans', 'toe beans',
            'murder mittens', 'airplane ears', 'chattering', 'chirping', 'slow blink',
            'cat tax', 'belly trap', 'catnip', 'cat tree', 'scratching post',
            'laser pointer', 'cat toys', 'cardboard box', 'if it fits i sits',
            'caturday', 'purrito', 'catloaf', 'nip', 'rescue cat', 'nine lives',
            'curiosity killed the cat', "cat's pajamas", 'scaredy cat', 'cool cat',
            'copy cat', 'catitude', 'catsplay', 'cat burglar', 'whisker fatigue'
        }

    def process_titles(self) -> list[str]:
        processed_titles = []
        for submission in self.client.subreddit("aww").top(time_filter="day", limit=5):
            processed_titles.append("".join(char for char in submission.title if char not in string.punctuation).lower())
        return processed_titles
    

    
    

    
if __name__ == "__main__":


    reddit = RedditClient(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
    )
    print(reddit.process_titles())

    
    
    
