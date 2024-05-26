from eth_account.account import Account
from coincurve.keys import PrivateKey, PublicKey
from eth_utils.crypto import keccak
from eth_utils.encoding import big_endian_to_int
import hashlib
import bech32

Account.enable_unaudited_hdwallet_features()


class AccountWarpper:
    def __init__(self, evm_account: Account):
        self.evm_account: Account = evm_account

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
            # lambda x: bech32_extension(x, hrp="", evm_compatible=False)
        ])

def bech32_extension(waccount: AccountWarpper, hrp: str = "cosmos", evm_compatible=False):
    if not evm_compatible:
        pubbytes = waccount.public_key_obj.format(compressed=True)
        s = hashlib.new("sha256", pubbytes).digest()
        r = hashlib.new("ripemd160", s).digest()
    else:
        r = waccount.account_bytes

    five_bit_r = bech32.convertbits(r, 8, 5)
    assert five_bit_r is not None
    waccount.derived_accounts[hrp] = \
        bech32.bech32_encode(hrp, five_bit_r)
    return waccount.derived_accounts[hrp]


def cosmos_extension(x): return bech32_extension(x, "cosmos")
def evmos_extension(x): return bech32_extension(x, "evmos", True)


if __name__ == "__main__":
    acc, mnemonic = Account.create_with_mnemonic(num_words=24)
    wacc = AccountWarpper(acc)
    wacc.exec_extension([cosmos_extension, evmos_extension])
    print(wacc)
