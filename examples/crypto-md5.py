from cryptography.hazmat.primitives import hashes
from Crypto.Hash import MD5 as pycrypto_md5
import hashlib

hashlib.md5(1)
hashlib.md5(1).hexdigest()

abc = str.replace(hashlib.md5("1"), "###")

print(hashlib.md5("1"))

pycrypto_md5.new()

hashes.MD5()
