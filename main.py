
from eth_account.hdaccount import generate_mnemonic
from core.account.account_manager import AccountManager


if __name__ == "__main__":
    mnemonic = generate_mnemonic(num_words=24, lang="english")
    am = AccountManager(mnemonic=mnemonic)
    am.create_account(10, verbose=True, with_bech32_extension=True)
