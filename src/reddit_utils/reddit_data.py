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
        self.dog_word_lists = {
            'doggo', 'pupper', 'good boy', 'good girl', 'bork', 'woof', 'puppy eyes',
            'snoot', 'belly rub', 'ear scratch', 'head tilt', 'tippy taps', 'wigglebutt',
            'doggo language', 'puppy tax', 'dog tax', 'rescue dog', 'mutt', 'purebred',
            'dog park', 'puppy kindergarten', 'dog training', 'positive reinforcement',
            'treat', 'boop the snoot', "who's a good boy", "who's a good girl", 'dog'
        }
        self.cat_word_lists = {
            'catto', 'kitty', 'kitten', 'purr', 'meow', 'beans', 'toe beans',
            'murder mittens', 'airplane ears', 'chattering', 'chirping', 'slow blink',
            'cat tax', 'belly trap', 'catnip', 'cat tree', 'scratching post',
            'laser pointer', 'cat toys', 'cardboard box', 'if it fits i sits',
            'caturday', 'purrito', 'catloaf', 'nip', 'rescue cat', 'nine lives',
            'curiosity killed the cat', "cat's pajamas", 'scaredy cat', 'cool cat',
            'copy cat', 'catitude', 'catsplay', 'cat burglar', 'whisker fatigue', 'cat',
            'car'
        }
        self.titles = ""
        self.majority = ""

    def process_titles(self, num_posts: int = 5) -> list[str]:
        """
        Returns specified number of top posts the previous day to transform to lowercase and removes punctuation.

        Args:
            num_posts (int): Number of posts to retrieve

        Returns:
            list[str]: A processed list of the top number of posts (lowercase and no punctuation)
        """
        processed_titles = []
        for submission in self.client.subreddit("aww").top(time_filter="day", limit=num_posts):
            processed_titles.append("".join(char for char in submission.title if char not in string.punctuation).lower())
        self.titles = processed_titles
        return processed_titles
    
    def get_majority(self) -> str:
        """
        Determines if the majority of top posts are related to cats or dogs.

        Returns:
            str: "dogs" if majority are dogs, "cats" if majority are cats else "equal
        """
        counts = {
            "dogs": 0,
            "cats": 0,
        }

        for title in self.titles:
            if any(keyword in title for keyword in self.dog_word_lists):
                counts["dogs"] += 1
            if any(keyword in title for keyword in self.cat_word_lists):
                counts["cats"] += 1
        
        if counts["dogs"] == counts["cats"]:
            return "equal"
        else:
            return max(counts, key=counts.get)
    

    
if __name__ == "__main__":


    reddit = RedditClient(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
    )
    print(reddit.process_titles(20))
    print("\n------\n")
    print(reddit.get_majority())

    
    
    
