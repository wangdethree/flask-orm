import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def aes_decrypt(encrypted_data: str, key: str) -> str:
    key_bytes = key.encode("utf-8")
    raw = base64.b64decode(encrypted_data)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


def aes_encrypt(plaintext: str, key: str) -> str:
    import os as _os
    from Crypto.Util.Padding import pad

    key_bytes = key.encode("utf-8")
    iv = _os.urandom(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode("utf-8")
