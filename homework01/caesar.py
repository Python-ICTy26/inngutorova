import typing as tp

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for i in plaintext:
        if (65 <= ord(i) <= 90-shift) or (97 <= ord(i) <= 122-shift):
            ciphertext += chr(ord(i) + shift)
        elif (90-shift+1 <= ord(i) <= 90) or (122-shift+1 <= ord(i) <= 122):
            ciphertext += chr(ord(i) - 26 + shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for i in ciphertext:
        if (65+shift <= ord(i) <= 90) or (97+shift <= ord(i) <= 122):
            plaintext += chr(ord(i) - shift)
        elif (65 <= ord(i) <= 65+shift-1) or (97 <= ord(i) <= 97+shift-1):
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

