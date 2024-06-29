from eth_account.account import Account, ETHEREUM_DEFAULT_PATH
from eth_account.signers.local import LocalAccount
from coincurve.keys import PrivateKey, PublicKey
from eth_utils.crypto import keccak
from eth_utils.encoding import big_endian_to_int
import hashlib
import bech32
from substrateinterface import Keypair

Account.enable_unaudited_hdwallet_features()


def get_keys(account: LocalAccount):
    private_key: PrivateKey = account._key_obj
    public_key: PublicKey = private_key.public_key
    public_key_bytes = public_key.to_bytes()
    point = (
        big_endian_to_int(public_key_bytes[:32]),
        big_endian_to_int(public_key_bytes[32:])
    )
    public_key_obj: PublicKey = PublicKey.from_point(*point)
    return private_key, public_key_obj


class AccountWarpper:
    def __init__(self,
                 mnemonic: str = "",
                 passphrase: str = "",
                 derive_path: str = ETHEREUM_DEFAULT_PATH):

        evm_account = Account.from_mnemonic(
            mnemonic=mnemonic,
            account_path=derive_path,
            passphrase=passphrase)

        self.account: LocalAccount = evm_account
        self.mnemonic: str = mnemonic
        self.passphrase: str = passphrase
        self.derive_path: str = derive_path

        self.private_key: PrivateKey = evm_account._key_obj
        self.private_key_bytes = self.private_key.to_bytes()
        self.public_key: PublicKey = self.private_key.public_key

        self.address: str = '0x' + \
            keccak(self.public_key.to_bytes())[-20:].hex()

        self.account_bytes = bytes.fromhex(
            str.removeprefix(self.address, "0x"))

        public_key_bytes: bytes = self.public_key.to_bytes()
        self.public_key_raw: str = public_key_bytes.hex()

        point = (
            big_endian_to_int(public_key_bytes[:32]),
            big_endian_to_int(public_key_bytes[32:])
        )
        self.public_key_obj: PublicKey = PublicKey.from_point(*point)

        self.public_key_compress: str = self.public_key_obj.format(
            compressed=True).hex()

        self.derived_accounts = {
            "memo": self.mnemonic,
            "path": self.derive_path,
            "eth": self.address
        }

    def __repr__(self) -> str:
        pk = self.private_key
        return "============== ACCOUNT_WARPPER =================\n" + \
            "pk\t:\t" + str(pk) + "\n" + \
            "\n".join(["{}\t:\t{}".format(k, v)
                      for k, v in self.derived_accounts.items()])

    def exec_extension(self, extension_funcs):
        for func in extension_funcs:
            func(self)

    def with_bech32_accounts(self):
        self.exec_extension([
            cosmos_extension,
            evmos_extension,
            nubit_extension,
            # lambda x: bech32_extension(x, hrp="", evm_compatible=False)
        ])

    def with_substrate_accounts(self):
        self.exec_extension([
            kusama_extension, polkadot_extension,
            lambda x: substrate_extension(x)
        ])


def bech32_extension(
    waccount: AccountWarpper,
    hrp: str = "nubit",
    evm_compatible=False,
    purpose=40,
    coin_type=60,
):
    if not evm_compatible:
        derive_acc = waccount
        pubkey_obj = waccount.public_key_obj
        if purpose != 40 or coin_type != 60:
            # self defined purpose and coin types.
            account_path = "m/{}'/{}'/0'/0/{}".format(purpose, coin_type, 0)
            derive_acc = Account.from_mnemonic(
                mnemonic=waccount.mnemonic,
                account_path=account_path,
                passphrase=waccount.passphrase
            )
            pk, pubkey_obj = get_keys(derive_acc)
            waccount.derived_accounts[hrp + "/p"] = account_path
            waccount.derived_accounts[hrp + "/pk"] = pk
        pubbytes = pubkey_obj.format(compressed=True)
        s = hashlib.new("sha256", pubbytes).digest()
        r = hashlib.new("ripemd160", s).digest()
    else:
        r = waccount.account_bytes

    five_bit_r = bech32.convertbits(r, 8, 5)
    assert five_bit_r is not None
    waccount.derived_accounts[hrp] = \
        bech32.bech32_encode(hrp, five_bit_r)

    return waccount.derived_accounts[hrp]


def substrate_extension(waccount: AccountWarpper, ss58_format: int = 42):
    # pk = str.removeprefix(waccount.account.key.hex(), "0x")
    # skeypair = Keypair.create_from_mnemonic(
    #     mnemonic=waccount.mnemonic, ss58_format=ss58_format)

    uri = waccount.mnemonic + "/" + waccount.derive_path
    skeypair = Keypair.create_from_uri(suri=uri, ss58_format=ss58_format)
    ss58key = "ss58/{}".format(ss58_format)
    waccount.derived_accounts[ss58key] = skeypair.ss58_address
    waccount.derived_accounts[ss58key+"p"] = uri
    waccount.__setattr__("substrate_keypair", skeypair)
    return skeypair


def cosmos_extension(x): return bech32_extension(x, "cosmos")
def evmos_extension(x): return bech32_extension(x, "evmos", True)
def nillion_extension(x): return bech32_extension(x, "nillion", False)
def nubit_extension(x): return bech32_extension(x, "nubit", False, 44, 118)
def kusama_extension(x): return substrate_extension(x, 2)
def polkadot_extension(x): return substrate_extension(x, 0)


if __name__ == "__main__":
    # acc, mnemonic = Account.create_with_mnemonic(num_words=24)
    mnemonic = "aerobic goat foster hint pyramid van cruise behind swear vibrant skull add message exhaust turn chief stable civil banana across fold eye envelope page"
    wacc = AccountWarpper(mnemonic=mnemonic)
    # wacc.exec_extension(
    #     [substrate_extension, kusama_extension, polkadot_extension])
    wacc.with_bech32_accounts()

    print(wacc)
