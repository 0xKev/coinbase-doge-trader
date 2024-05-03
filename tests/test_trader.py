from dotenv import load_dotenv
import os
import sys
sys.path.append("..")

from trader import CoinbaseTrader


load_dotenv()
SANDBOX_API_KEY = os.getenv("SANDBOX_API_KEY")
SANDBOX_PRIVATE_KEY = os.getenv("SANDBOX_PRIVATE_KEY")

trader = CoinbaseTrader(SANDBOX_API_KEY, SANDBOX_PRIVATE_KEY)

print(trader.list_accounts())