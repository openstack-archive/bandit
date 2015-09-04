from Crypto.Cipher import AES
from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4
from Crypto.Cipher import Blowfish
from Crypto.Cipher import DES
from Crypto.Cipher import DES3
from Crypto.Cipher import blockalgo
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers.modes import ECB


# Insecure mode
cipher = AES.new(key, AES.MODE_ECB, iv)

# Insecure cipher and mode
cipher = ARC2.new(key, ARC2.MODE_ECB, iv)

# Insecure cipher and mode
cipher = Blowfish.new(key, Blowfish.MODE_ECB, iv)

# Insecure mode
cipher = CAST.new(key, CAST.MODE_ECB, iv)

# Insecure cipher and mode
cipher = DES.new(key, DES.MODE_ECB, iv)

# Insecure mode
cipher = DES3.new(key, DES3.MODE_ECB, iv)

# Insecure mode
cipher = AES.new(key, blockalgo.MODE_ECB, iv)

# Insecure mode
mode = ECB(iv)

# Secure cipher and mode
cipher = AES.new(key, blockalgo.MODE_CTR, iv)

# Secure mode
mode = CBC(iv)
