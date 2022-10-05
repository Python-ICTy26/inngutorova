from caesar import decrypt_caesar, encrypt_caesar


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    for i in range(len(plaintext)):
        if ord("A") <= ord(keyword[i % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[i % len(keyword)]) - ord("A")
        else:
            shift = ord(keyword[i % len(keyword)]) - ord("a")
        ciphertext += encrypt_caesar(plaintext[i], shift)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    for i in range(len(ciphertext)):
        if ord("A") <= ord(keyword[i % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[i % len(keyword)]) - ord("A")
        else:
            shift = ord(keyword[i % len(keyword)]) - ord("a")
        plaintext += decrypt_caesar(ciphertext[i], shift)
    return plaintext
