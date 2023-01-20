import math
import string
import sys


def debug(*s):
    print(*s, file=sys.stderr, flush=True)

# decipher Vigenère cipher

encrypted_text_length = int(input())  # The length of the ecrypted message.
encrypted_text = input()  # The ecrypted message.
key_length = int(input())  # The length of secret key.
key = input()  # The secret key.

if key_length/encrypted_text_length < 1.0:
    times = math.ceil(encrypted_text_length / key_length)
    key=key*times

def process(e,k):
    shift = -string.ascii_uppercase.index(k)

    debug(e, k, shift)
    if e not in string.ascii_letters:
        return e

    new_idx = (string.ascii_uppercase.index(e) + shift) % 26
    return string.ascii_uppercase[new_idx]

result=[]
for e,k in zip(encrypted_text.upper(), key):
    result.append(process(e,k))

print("".join(result))
