from openmarket.lib import bech32
from secp256k1 import PrivateKey
from secrets import token_bytes
from mnemonic import Mnemonic
from bip32 import BIP32

mnemonic = Mnemonic("english")

class KeyChain:

    @staticmethod
    def to_mnemonic(seed: bytes = token_bytes(32)) -> str:
        return mnemonic.to_mnemonic(seed)
    
    @staticmethod
    def to_seed(words: str, passphrase: str = ""):
        return mnemonic.to_seed(words, passphrase)
    
    @staticmethod
    def to_nsec(seed: bytes) -> str:
        nsec = bech32.convertbits(BIP32.from_seed(seed).get_privkey_from_path(r"m/44'/1237'/0'/0/0"), 8, 5)
        return bech32.bech32_encode("nsec", nsec, bech32.Encoding.BECH32)

    @staticmethod
    def from_nsec(nsec: str) -> bytes:
        _, data, _ = bech32.bech32_decode(nsec)
        return bytes(bech32.convertbits(data, 5, 8)[:-1])
    
    @staticmethod
    def to_npub(nsec: str) -> str:
        npub = bech32.convertbits(PrivateKey(KeyChain.from_nsec(nsec)).pubkey.serialize()[1:], 8, 5)
        return bech32.bech32_encode("npub", npub, bech32.Encoding.BECH32)

    @staticmethod
    def from_npub(npub: str) -> bytes:
        _, data, _ = bech32.bech32_decode(npub)
        return bytes(bech32.convertbits(data, 5, 8)[:-1])