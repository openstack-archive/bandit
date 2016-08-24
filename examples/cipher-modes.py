from cryptography.hazmat.primitives.ciphers import modes


# Insecure mode
mode = modes.ECB(iv)

# Secure cipher and mode
cipher = AES.new(key, blockalgo.MODE_CTR, iv)

# Secure mode
mode = modes.CBC(iv)
