import os
import sys
import math
import hashlib
import re
import binascii
import unicodedata

"""            """
# Test sentence
# thrive call mistake crack glare sustain expand lend tip install camp patient

def check_phrase(twelve_eleven):
    
    deb = twelve_eleven[:128]
    fin = twelve_eleven[-4:]

    deb_hex = hex(int(deb,2))

    deb_byte = binascii.a2b_hex(deb_hex[2:]) # Hex to Byte
    
    hash_256 = hashlib.sha256(deb_byte).hexdigest() 
    checksum = bin(int(hash_256, 16))[2:].zfill(128)[:4]

    if checksum == fin:
        print("\nThe mnemonic corresponds to the BIP 39 standard\nHere is the checksum and the last 4 bit of the Hash :\n", checksum, fin)
        return(True)
    if checksum != fin: 
        print("\nThe seed you entered isn't correct. Try again !\n") 
        return(False)

def get_phrase_from_user(phrase):
    phrase = re.sub("[^\w]", " ",  phrase).split()

    with open("english.txt", "r") as f:
        wordlist = [w.strip() for w in f.readlines()]
    
    twelve_eleven = ""

    for word in phrase:
        try:
            index = bin(wordlist.index(word))[2:]
        except:
            print("\nYour word is not in BIP39 list, try again")
            exit()
        index = '0'*(11-len(index)) + index
        twelve_eleven += index
    print("\nAll your words are in the BIP39 list")
    check_phrase(twelve_eleven)
    return(twelve_eleven)

def get_rand_phrase():

    bits = 128
    bytes = bits//8 # =16

    rand = os.urandom(bytes) 

    rand_hex = binascii.b2a_hex(rand) # Bytes to hex
    print("\nHere is the random int generate with urandom :\n", int(rand_hex,16))

    checksum_length = bits//32

    hash_256 = hashlib.sha256(rand).hexdigest() # Hash in Hex

    entropy = bin(int(rand_hex, 16))[2:].zfill(bits)
    checksum = bin(int(hash_256, 16))[2:].zfill(bits)[:checksum_length]

    twelve_eleven = entropy + checksum

    check_phrase(twelve_eleven)
    dic = []
    with open("english.txt", "r") as f:
        for w in f.readlines():
            dic.append(w.strip())
   
    print("\nThis is all the twelve eleven bits, their integer and their words associate :")
    wordlist = []
    for i in range(len(twelve_eleven) // 11):
        index_bin = twelve_eleven[11*i : 11*(i+1)]
        index = int(index_bin,2) # In base 2
        wordlist.append(dic[index])
        print(i+1, index_bin, " | " , dic[index])

    phrase = ' '.join(wordlist)
    print(f"\nThis is your mnemonic phrase :\n{phrase}\n")

    
    return(phrase)

def get_seed_from_phrase(phrase):
    normalized_mnemonic = unicodedata.normalize("NFKD", phrase)
    password = ""
    normalized_passphrase = unicodedata.normalize("NFKD", password)

    passphrase = "mnemonic" + normalized_passphrase
    mnemonic = normalized_mnemonic.encode("utf-8")
    passphrase = passphrase.encode("utf-8")

    seed = hashlib.pbkdf2_hmac("sha512", mnemonic, passphrase, 2048)
    print("\nThis is your BIP39 Seed :\n", binascii.hexlify(seed[:64]))

    print("\nPlease note that this seed is a perfect match with the Mnemonic on this website:\nhttps://iancoleman.io/bip39/\n\n")

    return(seed)
    
  

if __name__ == "__main__":

    print(f"\nType enter to get a seed or type your's with spaces.\n")
    choice = input()
    if choice == "":
        phrase = get_rand_phrase()
    else:
        phrase = get_phrase_from_user(choice)

    seed = get_seed_from_phrase(phrase)
    
    





