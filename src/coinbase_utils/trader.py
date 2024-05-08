import os
from dotenv import load_dotenv
from coinbase import jwt_generator
from coinbase.rest import RESTClient
from json import dumps
from time import time

load_dotenv()
COINBASE_API_KEY_NAME = os.getenv("COINBASE_API_KEY")
COINBASE_PRIVATE_KEY = os.getenv("COINBASE_PRIVATE_KEY")

# NOT NECESSARY BECAUSE COINBASE SDK HANDLES IT AUTOMATICALLY BUT KEEP JUST IN CASE
def build_jwt(request_method: str, request_path: str) -> str: 
    # each jwt expires after 2 min, must generate new jwt for each unique api requests
    jwt_uri = jwt_generator.format_jwt_uri(
        method=request_method, 
        path=request_path
    )
    jwt_token = jwt_generator.build_rest_jwt(
        uri=jwt_uri,
        key_var=COINBASE_API_KEY_NAME,
        secret_var=COINBASE_PRIVATE_KEY
    )
    return jwt_token

# get uuid of doge is doge wallet exists
# otherwise get doge uuid after making first purchase
# as longa s self.doge_uuid is None, create purchase and assign

class CoinbaseTrader:
    def __init__(self, api_key: str, api_secret: str) -> None:
        """
        Initializes a new instance of the Trader class.

        Args:
            COINBASE_API_KEY (str): The API key for accessing the Coinbase API.
            api_secret (str): The API secret for accessing the Coinbase API.
        """
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)
        self.wallets = {
            "doge": "DOGE Wallet",
            "usd": "Cash (USD)",
        }
        self.product_ids = {
            "doge": "DOGE-USD",
        }
        
        self.doge_uuid = self.get_uuid("doge")
        self.usd_uuid = self.get_uuid("usd")

        

    def list_accounts(self) -> dict[str, any]:
        """
        Retrieves a list of accounts associated with the Coinbase client
        
        Returns:
            dict[str, any]: A dictionary of all account information
        """
        return self.client.get_accounts()["accounts"]
    
    def get_uuid(self, wallet_name: str) -> str:
        """
        Retrives the UUID of the specified wallet

        Args:
            wallet_name (str): The wallet name

        Returns:
            str: The UUID of the specified account
        """

        accounts = self.list_accounts()
        for account in accounts:
            if account.get("name", None) == self.wallets[wallet_name]:
                return account.get("uuid", None)
            
    def get_acc_details(self, wallet_name: str) -> dict[str, any]:
        """
        Retrieves the specified account details

        Args:
            wallet_name (str): The wallet name
        
        Returns:
            dict[str, any]: A dictionary containing the specified account information
        """
        wallet_accounts = {
            "doge": self.doge_uuid,
            "usd": self.usd_uuid,
        }
        account_details = self.client.get_account(account_uuid=wallet_accounts[wallet_name])
        # dumps used to return as formatted json
        #return dumps(account_details, indent=2)
        return account_details
    
    def place_order(self, buy_cost: str = "1") -> bool:
        """
        Places a market order for DOGE coin if sufficient money

        Args:
            buy_cost (str): Amount of money in USD to spend on order
        
        Returns:
            bool: True if order placed successfully, else False
        """
        if self.check_balance("doge") - 1 <= buy_cost:
            # - 1 to consider fees
            order = self.client.market_order_buy(
                    client_order_id=str(int(time())),
                    product_id="DOGE-USD",
                    quote_size=buy_cost,
            )
            return order["success"]
    
    def sell_order(self, sell_cost: str = "1") -> bool:
        """
        Places a market sell order for the amount of DOGE coin specified

        Args:
            sell_cost (str): Amount of doge coin to sell (default 1)

        Returns:
            bool: True if order placed successfully, else False
        """
        usd_value = self.check_balance("doge")["doge"]["value"]
        sell_quantity = self.cost_to_quantity(cost=sell_cost)["ask_quantity"]
        
        if usd_value >= float(sell_cost):
            # -1 to consider fees
            sell_order = self.client.market_order_sell(
                client_order_id=str(int(time())),
                product_id="DOGE-USD",
                base_size=str(sell_quantity),
            )
            return sell_order["success"]
        
    def cost_to_quantity(self, cost: int = "1") -> dict[str, float]:
        """
        Determines the quantity of coins for bid and sell price from a specified cost

        Args:
            cost (int): The amount of money to convert to bid/ask quantity 
        
        Returns:
            dict[str, float]: A dictionary of the bid/ask with each quantity
        """
        cost = int(cost) # to accept both str and int
        bid_ask: dict[str, float] = self.get_bid_ask("doge")
        quantity = {
            "bid_quantity": round((cost / bid_ask["bid_price"]), 1),
            "ask_quantity": round((cost / bid_ask["ask_price"]), 1), 
        }
        return quantity

        
    def check_balance(self, wallet_name: str) -> dict[str, dict[str, float]]:
        """
        Checks the balance of specified wallet (doge/usd)

        Args:
            wallet_name (str): Name of wallet
        
        Returns:
            dict[str, dict[str, float]]: A dictionary containing wallet name as key and a dict of wallet balance and worth as value.
        """
        if wallet_name not in self.wallets:
            raise "Invalid wallet name."
        
        account = self.get_acc_details(wallet_name)["account"]
        balance = round(float(account["available_balance"]["value"]), 5)
        ask_price = self.get_bid_ask("doge")[1]
        value = round(ask_price * balance, 2)

        return {
            wallet_name: {
                "balance": balance, 
                "value": value
            }
        }

    def get_bid_ask(self, wallet_name: str = "doge") -> dict[str, float]:
        """
        Gets the bid and ask price of specified cryptocurrency

        Args:
            wallet_name (str): Name of coin

        Returns:
            dict[str, float]: A dictionary containg the bid and ask price
        """
        prices = self.client.get_best_bid_ask(self.product_ids[wallet_name])
        bid = float(prices["pricebooks"][0]["bids"][0]["price"])
        ask = float(prices["pricebooks"][0]["asks"][0]["price"])

        return {
            "bid_price": bid,
            "ask_price": ask,
        }
    
    
class SandboxCoinbaseTrader:
    # WILL ONLY WORK WITH EXCHANGE API
    # DOES NOT WORK WITH ADVANECD TRADE API 
    # DOES NOT WORK WITH OFFICIAL COINBASE SDK
    # no doge, will do btc
    # use generic REST calls due to different sandbox endpoints
    # REST API url https://api-public.sandbox.exchange.coinbase.com
    def __init__(self, COINBASE_API_KEY: str, api_secret: str) -> None:
        self.client = RESTClient(COINBASE_API_KEY=COINBASE_API_KEY, api_secret=api_secret)
        self.btc_uuid = self.get_btc_uuid()
        self.api_url = "https://api-public.sandbox.exchange.coinbase.com/accounts"


    def list_accounts(self) -> dict[str, any]:
        return self.client.get(url_path=self.api_url)
    
    def get_btc_uuid(self) -> str:
        accounts = self.list_accounts()
        for account in accounts:
            if account.get("name", None) == "BTC Wallet":
                return account.get("uuid", None)
            
    def get_btc_acc_details(self) -> dict[str, any]:
        account_details = self.client.get_account(account_uuid=self.btc_uuid)
        # dumps used to return as formatted json
        #return dumps(account_details, indent=2)
        return account_details
    
    
if __name__ == "__main__":
    pass