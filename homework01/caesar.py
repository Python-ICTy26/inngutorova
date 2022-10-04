import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for i in plaintext:
        if (ord('A') <= ord(i) <= ord('Z')-shift) or (ord('a') <= ord(i) <= ord('z')-shift):
            ciphertext += chr(ord(i) + shift)
        elif (ord('Z')-shift+1 <= ord(i) <= ord('Z')) or (ord('z')-shift+1 <= ord(i) <= ord('z')):
            ciphertext += chr(ord(i) - 26 + shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for i in ciphertext:
        if (ord('A')+shift <= ord(i) <= ord('Z')) or (ord('a')+shift <= ord(i) <= ord('z')):
            plaintext += chr(ord(i) - shift)
        elif (ord('A') <= ord(i) <= ord('A')+shift-1) or (ord('a') <= ord(i) <= ord('a')+shift-1):
            plaintext += chr(ord(i) + 26 - shift)
        else:
            plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
