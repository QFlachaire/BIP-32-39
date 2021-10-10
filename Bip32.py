import binascii
import hmac
import hashlib
import ecdsa
import base58 as B58
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa import int_to_string, string_to_int
import struct
import Bip39


def get_private_and_chain(seed):

    seed = binascii.unhexlify("000102030405060708090a0b0c0d0e0f")  # Choosen in order to verify result whith test vectors

    # Can add password if the user want to salt
    salt = b"Bitcoin seed" # Choosen in order to verify result whith test vectors
    h = hmac.new(salt, seed, hashlib.sha512).digest()

    master_private_key = h[:32]
    master_chain_code = h[32:]

    print("Your pvkey :\n", binascii.b2a_hex(master_private_key), "\nYour chaincode\n", binascii.b2a_hex(master_chain_code))
    
    return master_private_key, master_chain_code

def get_child_keys(master_private_key, master_chain_code, depth, index, fpr):

    xprv = binascii.unhexlify("0488ade4") #Mainnet version bytes "xpub"
    xpub = binascii.unhexlify("0488b21e") #Mainnet version bytes "xprv"
    child = struct.pack('>L', index)

    private_key = ecdsa.SigningKey.from_string(master_private_key, curve=SECP256k1)
    K_priv = private_key.get_verifying_key()

    priv = b'\x00' + (private_key.to_string())  # ser256(p): serializes integer p as a 32-byte sequence

    # serialization the coordinate pair P = (x,y) as a byte sequence using SEC1's compressed form
    if K_priv.pubkey.point.y() & 1:
        pub= b'\3'+int_to_string(K_priv.pubkey.point.x())
    else:
        pub = b'\2'+int_to_string(K_priv.pubkey.point.x())

    raw_priv = xprv + depth + fpr + child + master_chain_code + priv
    raw_pub = xpub + depth + fpr + child + master_chain_code + pub

    # Hash two times using SHA256
    hashed_xprv = hashlib.sha256(hashlib.sha256(raw_priv).digest()).digest()
    hashed_xpub = hashlib.sha256(hashlib.sha256(raw_pub).digest()).digest()

    # Add 4 bytes of checksum Befor encoding to Base 58
    raw_priv += hashed_xprv[:4]
    raw_pub += hashed_xpub[:4]

    # Return base58
    print("Your external private key :\n", B58.b58encode(raw_priv))
    print("Your external public key :\n", B58.b58encode(raw_pub))
    print("They are the same as the one one in the test vectors")
    return (raw_pub, raw_priv)




if __name__ == "__main__":

    seed = Bip39.get_seed_from_phrase(Bip39.get_rand_phrase())

    depth = bytes([0]) # Child depth; parent increments its own by one when assigning this
    fpr = b'\0\0\0\0' # Parent fingerprint,
    index = 0  # Child index
    master_private_key, master_chain_code = get_private_and_chain(seed)

    master_public_key, raw_priv = get_child_keys(master_private_key, master_chain_code, depth, index, fpr)
