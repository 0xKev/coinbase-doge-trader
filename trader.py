import os
from dotenv import load_dotenv
from coinbase import jwt_generator
from coinbase.rest import RESTClient
from json import dumps
from time import time

load_dotenv()
API_KEY_NAME = os.getenv("API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# NOT NECESSARY BECAUSE COINBASE SDK HANDLES IT AUTOMATICALLY BUT KEEP JUST IN CASE
def build_jwt(request_method: str, request_path: str) -> str: 
    # each jwt expires after 2 min, must generate new jwt for each unique api requests
    jwt_uri = jwt_generator.format_jwt_uri(
        method=request_method, 
        path=request_path
    )
    jwt_token = jwt_generator.build_rest_jwt(
        uri=jwt_uri,
        key_var=API_KEY_NAME,
        secret_var=PRIVATE_KEY
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
            api_key (str): The API key for accessing the Coinbase API.
            api_secret (str): The API secret for accessing the Coinbase API.
        """
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)
        self.doge_uuid = self.get_uuid("doge")
        self.usd_uuid = self.get_uuid("usd")

        self.wallets = {
            "doge": "DOGE Wallet",
            "usd": "Cash (USD)",
        }

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
            
    def get_acc_details(self) -> dict[str, any]:
        """
        Retrieves the DOGE coin account details

        Returns:
            dict[str, any]: A dictionary containing the DOGE coin account information
        """
        account_details = self.client.get_account(account_uuid=self.doge_uuid)
        # dumps used to return as formatted json
        #return dumps(account_details, indent=2)
        return account_details
    
    def place_order(self, buy_cost: str = "1") -> bool:
        """
        Places a market order for DOGE coin if sufficient money

        Args:
            buy_cost (str): Amount of money to spend on order
        
        Returns:
            bool: True if order placed successfully, else False
        """
        order = self.client.market_order_buy(
                client_order_id=str(int(time())),
                product_id="DOGE-USD",
                quote_size=buy_cost,
        )
        return order["success"]
    
    def check_balance(self) -> float:
        return 

    

    
    
class SandboxCoinbaseTrader:
    # WILL ONLY WORK WITH EXCHANGE API
    # DOES NOT WORK WITH ADVANECD TRADE API 
    # DOES NOT WORK WITH OFFICIAL COINBASE SDK
    # no doge, will do btc
    # use generic REST calls due to different sandbox endpoints
    # REST API url https://api-public.sandbox.exchange.coinbase.com
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)
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
    doge_trader = CoinbaseTrader(api_key=API_KEY_NAME, api_secret=PRIVATE_KEY)
    account = doge_trader.get_acc_details()
    print(doge_trader.list_accounts())