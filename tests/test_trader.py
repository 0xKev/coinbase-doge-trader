from dotenv import load_dotenv
import os
import sys
sys.path.append("../")

from src.coinbase_utils.trader import CoinbaseTrader


load_dotenv()
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
COINBASE_PRIVATE_KEY = os.getenv("COINBASE_PRIVATE_KEY")

trader = CoinbaseTrader(api_key=COINBASE_API_KEY, api_secret=COINBASE_PRIVATE_KEY)
res = trader.check_balance("usd")

print(res)

#print(trader.get_acc_details("usd"))