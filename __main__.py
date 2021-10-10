import Bip39
import Bip32


if __name__ == "__main__":

    print(f"\nPress enter to get a seed or type your's with spaces.\n")
    choice = input()
    if choice == "":
        phrase = Bip39.get_rand_phrase()
    else:
        phrase = Bip39.get_phrase_from_user(choice)

    seed = Bip39.get_seed_from_phrase(phrase)

    depth = bytes([1]) # Child depth
    fpr = b'\0\0\0\0' # Parent fingerprint,
    index = 1  # Child index
    master_private_key, master_chain_code = Bip32.get_private_and_chain(seed)

    master_public_key, raw_priv = Bip32.get_child_keys(master_private_key, master_chain_code, depth, index, fpr)
