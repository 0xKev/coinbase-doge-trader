import os
from dotenv import load_dotenv
from coinbase import jwt_generator
from coinbase.rest import RESTClient
from json import dumps

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
    # most likely trading doge and looking through reddit for dog pics
    # doge uuid "e47aa869-9f80-504e-b130-23ec7ca40667"
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)
        self.doge_uuid = self.get_doge_uuid()


    def list_accounts(self) -> dict[str, any]:
        return self.client.get_accounts()["accounts"]
    
    def get_doge_uuid(self) -> str:
        accounts = self.list_accounts()
        for account in accounts:
            if account.get("name", None) == "DOGE Wallet":
                return account.get("uuid", None)
            
    def get_doge_acc_details(self) -> dict[str, any]:
        account_details = self.client.get_account(account_uuid=self.doge_uuid)
        # dumps used to return as formatted json
        #return dumps(account_details, indent=2)
        return account_details
    
class SandboxCoinbaseTrader:
    # no doge, will do btc
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = RESTClient(api_key=api_key, api_secret=api_secret)
        self.btc_uuid = self.get_btc_uuid()


    def list_accounts(self) -> dict[str, any]:
        return self.client.get_accounts()["accounts"]
    
    def get_btc_uuid(self) -> str:
        accounts = self.list_accounts()
        for account in accounts:
            if account.get("name", None) == "BTC Wallet":
                return account.get("uuid", None)
            
    def get_doge_acc_details(self) -> dict[str, any]:
        account_details = self.client.get_account(account_uuid=self.doge_uuid)
        # dumps used to return as formatted json
        #return dumps(account_details, indent=2)
        return account_details
if __name__ == "__main__":
    doge_trader = CoinbaseTrader(api_key=API_KEY_NAME, api_secret=PRIVATE_KEY)
    account = doge_trader.get_doge_acc_details()
    print(doge_trader.list_accounts())