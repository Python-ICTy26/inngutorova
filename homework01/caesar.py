import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    shift = shift % 26
    for i in plaintext:
        if (ord("A") <= ord(i) <= ord("Z") - shift) or (ord("a") <= ord(i) <= ord("z") - shift):
            ciphertext += chr(ord(i) + shift)
        elif (ord("Z") - shift + 1 <= ord(i) <= ord("Z")) or (ord("z") - shift + 1 <= ord(i) <= ord("z")):
            ciphertext += chr(ord(i) - 26 + shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
