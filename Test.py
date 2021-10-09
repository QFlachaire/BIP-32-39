import os
import sys
import math
import hashlib


rand = os.urandom(16) 
entropy = bin(int.from_bytes(rand, "big"))[2:]
hash_256 = hashlib.sha256(entropy.encode()).digest() #hash en hexadécimal

four_bits = bin(int.from_bytes(hash_256, "big"))[2:6]
print(len(entropy))
print(len(four_bits))
twelve_eleven = entropy + four_bits
print(len(twelve_eleven))