
from web3 import Web3, Account


def print_(x): return print(">>> {}".format(x))


class AccountManager(object):
    def __init__(self, mnemonic="",
                 derive_path_format: str = "",
                 password=""):
        self.mnemonic = mnemonic
        self.derive_path_format = derive_path_format if derive_path_format != "" else "m/40'/60'/0'/0/{}"
        self.accounts = []
        self.password = password
        self.extra = {}

    def get_account(self, index=0) -> Account:
        if index > len(self.accounts)-1:
            raise KeyError(
                f'the index {index} is exceed total account num {len(self.accounts)}.')
        return self.accounts[index]

    def create_account(self, count=1, verbose=False):
        for i in range(count):
            idx = len(self.accounts)
            derive_path = self.derive_path_format.format(idx)
            evm_account = Account.from_mnemonic(
                mnemonic=self.mnemonic, account_path=derive_path,
                passphrase=self.password)
            if verbose:
                print("{},{},{},{}".format(idx, evm_account.address,
                      evm_account.key.hex(), derive_path))
            # print_("#{} generated new account by path {}".format(i, derive_path))
            # print_("\t\t\t Public key: {}".format(evm_account.address))
            self.accounts.append(evm_account)
        return self.accounts

    def export_dict(self):
        export = []
        for idx, account in enumerate(self.accounts):
            add = Web3.to_checksum_address(account.address)
            pk = account.key.hex()
            export.append({
                "id": idx,
                "address": add,
                "pk": pk
            })
        return export

    def query_account_balance(self, index, w3):
        account = self.get_account(index=index)
        balance = w3.from_wei(w3.eth.get_balance(account.address), "ether")
        return float(balance)

    def query_balance(self, w3):
        balance_detail = []
        for i in range(len(self.accounts)):
            balance = w3.from_wei(w3.eth.get_balance(
                self.accounts[i].address), "ether")
            balance_detail.append((i, self.accounts[i].address, balance))
            print("# {}, {}: balance: {} eth".format(
                i, self.accounts[i].address, balance))
        return balance_detail

    def query_balances(self, w3_map: dict, verbose=False):
        for i in range(len(self.accounts)):
            if verbose:
                print("# ---------------------------------------------------------")
                print("# {}, {}".format(i, self.accounts[i].address))
            for name, w3 in w3_map.items():
                balance = w3.from_wei(w3.eth.get_balance(
                    self.accounts[i].address), "ether")
                if verbose:
                    print("#    {:.5f} ETH on [{}]".format(balance, name))
