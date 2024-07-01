import os
if not os.path.exists("data/agents"):
    os.makedirs("data/agents")
from .account import AccountWarpper
from .account_manager import AccountManager
from eth_account.account import ETHEREUM_DEFAULT_PATH


class Agent(object):

    # thread safe Agent both interact with web3 and web2.
    def __init__(
            self, 
            name: str, 
            mnemonic: str, 
            password: str="",
            account_derive_path: str=ETHEREUM_DEFAULT_PATH,
            slaves_derive_path: str=ETHEREUM_DEFAULT_PATH,
            slaves_count: int=100,
            discord_info: dict=None,
            twitter_info: dict=None
        ) -> None:

        self.name = name
        # web3
        self.account_warpper: AccountWarpper = \
            AccountWarpper(
                mnemonic=mnemonic,
                derive_path=account_derive_path,
                passphrase=password)

        
        slaves_manager = AccountManager(
            mnemonic=mnemonic, 
            derive_path_format=slaves_derive_path,
            password=password)
        
        slaves_manager.create_account(slaves_count)
        
        self.slaves_manager = slaves_manager
        
        # web2
        self.headers = {}
        self.discord = discord_info
        self.twitter = twitter_info
        
        
        self.ctx = {}

    def __setitem__(self, key, val):
        self.ctx[key] = val
        
    def __getitem__(self, key):
        return self.ctx.get(key, None)


    def export_account(self, verbose=False):
        if verbose:
            print(self.ctx)
        
        return {
            
        }.update(self.ctx)

    def restore_account(self, verbose=False):
        return None

