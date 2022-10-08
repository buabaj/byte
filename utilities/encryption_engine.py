import rsa

privateKey, publicKey = rsa.newkeys(512)


def encrypt(message):
    return rsa.encrypt(message.encode(), publicKey)


def decrypt(message):
    return rsa.decrypt(message, privateKey).decode()
