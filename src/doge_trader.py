from dotenv import load_dotenv
from os import getenv
from coinbase_utils.trader import CoinbaseTrader
from reddit_utils.reddit_data import RedditClient



class AutoTrader:
    def __init__(self, coinbase_trader: CoinbaseTrader, reddit_client: RedditClient):
        self.coinbase_trader = coinbase_trader
        self.reddit_client = reddit_client
        self.actions = {
            "dogs": self.coinbase_trader.place_order,
            "cats": self.coinbase_trader.sell_order,
        }

    def run(self):
        self.reddit_client.process_titles(60)
        majority = self.reddit_client.get_majority()
        print(majority)



def main():
    load_dotenv()
    COINBASE_API_KEY = getenv("COINBASE_API_KEY")
    COINBASE_PRIVATE_KEY = getenv("COINBASE_PRIVATE_KEY")

    REDDIT_API_KEY = getenv("REDDIT_CLIENT_ID")
    REDDIT_PRIVATE_KEY = getenv("REDDIT_CLIENT_SECRET")

    coinbase_trader = CoinbaseTrader(
        api_key=COINBASE_API_KEY,
        api_secret=COINBASE_PRIVATE_KEY 
    )

    reddit_client = RedditClient(
        client_id=REDDIT_API_KEY,
        client_secret=REDDIT_PRIVATE_KEY
    )

    auto_trader = AutoTrader(
        coinbase_trader=coinbase_trader,
        reddit_client=reddit_client
    )
    auto_trader.run()

if __name__ == "__main__":
    main()