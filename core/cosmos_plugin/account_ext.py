import hashlib

import bech32
import ecdsa
import hdwallets
import mnemonic
from typing import TypedDict
from web3 import Account
Account.enable_unaudited_hdwallet_features()

DEFAULT_DERIVATION_PATH = "m/44'/118'/0'/0/0"
DEFAULT_BECH32_HRP = "cosmos"

"""
https://docs.cosmos.network/v0.50/learn/beginner/accounts
"""


class CosmosAccountExtension(object):
    def __init__(
            self,
            menmonic="",
            passphrase="",
            hrp=DEFAULT_BECH32_HRP,
            hdpath=DEFAULT_DERIVATION_PATH,
            **kwargs) -> None:

        self.coin_type = kwargs.get("coin_type", None)
        self.denom = kwargs.get("denom", None)
        self.menmonic = menmonic.replace("-", " ")

    @staticmethod
    def __after_account_generate(account: Account):
        hdwallet = hdwallets.BIP32.from_seed(account.key)
        bech32.encode()


if __name__ == "__main__":
    ETHEREUM_DEFAULT_PATH = "m/44'/60'/0'/0/0"
    acct, mnemonic_phrase = Account.create_with_mnemonic()
    print("evm pk\t\t",acct.key.hex())
    
    print("evm addr\t",acct.address)
    from coincurve.keys import PrivateKey

    private_key: PrivateKey = acct._key_obj
    print("evm pub\t\t", acct._key_obj.public_key.to_bytes().hex())
    print(private_key.public_key.to_bytes().hex())
    # acct_pub_key = acct._key_obj.public_key.to_bytes()
    # pub_key.format(compressed=True)
    from coincurve.keys import PublicKey
    from eth_utils.encoding import big_endian_to_int
    point = (
        big_endian_to_int(acct._key_obj.public_key.to_bytes()[:32]),
        big_endian_to_int(acct._key_obj.public_key.to_bytes()[32:])
    )
    public_key_obj = PublicKey.from_point(*point)
    compressed_pub = public_key_obj.format(compressed=True)
    raw_pub = public_key_obj.format(compressed=False)
    
    from eth_utils.crypto import keccak
    address = keccak(acct._key_obj.public_key.to_bytes())[-20:]
    
    print("evm cpub\t", compressed_pub.hex())
    print("evm address\t", address.hex())
    print("evm rawpub\t", raw_pub.hex()[-128:])
    # -----------------------------------------------------------
    
    print("-------------------------------------------------------------")
    seed = mnemonic.Mnemonic.to_seed(mnemonic=mnemonic_phrase, passphrase="")
    hdwallets = hdwallets.BIP32.from_seed(seed=seed)
    pk = hdwallets.get_privkey_from_path(ETHEREUM_DEFAULT_PATH)
    print("cos pk\t\t", "0x" + pk.hex())
    privkey_obj = ecdsa.SigningKey.from_string(pk, curve=ecdsa.SECP256k1)
    pubkey_obj = privkey_obj.get_verifying_key().to_string("raw")
    
    
    print("cos pubkey raw\t", pubkey_obj.hex())
    pubkey_obj = privkey_obj.get_verifying_key().to_string("compressed")
    print("cos pubkey cmpr\t", pubkey_obj.hex())
    