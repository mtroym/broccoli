
from web3 import Web3, Account
from .account import AccountWarpper


class AccountManager(object):
    def __init__(self, mnemonic="",
                 derive_path_format: str = "",
                 password=""):
        self.mnemonic = mnemonic
        self.derive_path_format = derive_path_format if derive_path_format != "" else "m/40'/60'/0'/0/{}"
        self.accounts: list = []
        self.password = password
        self.extra = {}
        self.warppers = []

    def get_account(self, index=0) -> Account:
        if index > len(self.accounts)-1:
            raise KeyError(
                f'the index {index} is exceed total account num {len(self.accounts)}.')
        return self.accounts[index]

    def create_account(self, count=1, verbose=False,
                       with_bech32_extensions=False,
                       with_substrate_extenstions=False):
        for i in range(count):
            idx = len(self.accounts)
            derive_path = self.derive_path_format.format(idx)
            # evm_account = Account.from_mnemonic(
            #     mnemonic=self.mnemonic, account_path=derive_path,
            #     passphrase=self.password)
            warpper = AccountWarpper(mnemonic=self.mnemonic,
                                     passphrase=self.password,
                                     derive_path=derive_path)

            evm_account = warpper.account
            if with_bech32_extensions:
                warpper.with_bech32_accounts()
            if with_substrate_extenstions:
                warpper.with_substrate_accounts()

            if verbose:
                print(warpper)
                print()
                # print("{},{},{},{}".format(idx, evm_account.address,
                #       evm_account.key.hex(), derive_path))
            # print_("#{} generated new account by path {}".format(i, derive_path))
            # print_("\t\t\t Public key: {}".format(evm_account.address))
            self.accounts.append(evm_account)
            self.warppers.append(warpper)
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


if __name__ == "__main__":
    acc, mnemonic = Account.create_with_mnemonic()
    am = AccountManager(mnemonic=mnemonic)
    am.create_account(10, verbose=True, with_bech32_extensions=True)
