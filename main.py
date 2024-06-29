
from eth_account.hdaccount import generate_mnemonic
from core.resource import AccountManager, AccountWarpper

if __name__ == "__main__":
    mnemonic = generate_mnemonic(num_words=24, lang="english")
    am = AccountManager(mnemonic=mnemonic)
    am.create_account(1, verbose=False,
                      with_bech32_extensions=True,
                      with_substrate_extenstions=False)
    accwarpper: AccountWarpper = am.warppers[0]
    print(accwarpper.derived_accounts["nubit"])
