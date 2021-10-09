import os
import sys
import math
import hashlib
import re

# Test sentence
# pudding bottom soldier breeze educate grass order oxygen pottery crystal tongue among

def get_seed():
    seed = []
    print(f"sentence or word by word (word) ?")
    rep = input()

    if rep == "word":
        for i in range(1, 13, 1):
            print(f"Write your word {i} :")
            seed.append(input())
    else:
        print(f"Write your sentence:")
        seed = re.sub("[^\w]", " ",  input()).split()
    print(seed)
    return(seed)

def get_rand_seed():

    rand = os.urandom(16) 
    entropy = bin(int.from_bytes(rand, "big"))[2:]
    hash_256 = hashlib.sha256(entropy.encode()).digest() #hash en hexadécimal

    four_bits = bin(int.from_bytes(hash_256, "big"))[2:6]
    print(len(entropy))
    print(len(four_bits))
    twelve_eleven = entropy + four_bits
    print(len(twelve_eleven))
    with open("english.txt", "r") as f:
        wordlist = [w.strip() for w in f.readlines()]

    seed = []
    for i in range(0, 12, 1):
        indx = int(twelve_eleven[11*i:11*(i+1)])
        seed.append(wordlist[indx])
    return(seed)

    





if __name__ == "__main__":

    print(f"Enter your seed or type rand to get a new one")
    choice = input()
    if choice == "rand":
        seed = get_rand_seed()
    else:
        seed = get_seed()





