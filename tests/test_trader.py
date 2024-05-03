from dotenv import load_dotenv
import os
import sys
sys.path.append("..")

from trader import CoinbaseTrader


load_dotenv()
API_KEY = os.getenv("API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

trader = CoinbaseTrader(api_key=API_KEY, api_secret=PRIVATE_KEY)
res = trader.check_balance("usd")

print(res)

#print(trader.get_acc_details("usd"))