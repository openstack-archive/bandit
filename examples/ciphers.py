from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4
from Crypto.Cipher import Blowfish
from Crypto.Cipher import DES
from Crypto.Cipher import XOR
from Crypto.Hash import SHA
from Crypto.Util import Counter
from struct import pack

key = b'Sixteen byte key'
iv = b'01010101'
cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
msg = iv + cipher.encrypt(b'Attack at dawn')

key = b'Very long and confidential key'
nonce = b'0101010101010101'
tempkey = SHA.new(key+nonce).digest()
cipher = ARC4.new(tempkey)
msg = nonce + cipher.encrypt(b'Open the pod bay doors, HAL')

bs = Blowfish.block_size
key = b'An arbitrarily long key'
iv = b'0101010101010101'
cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
plaintext = b'docendo discimus '
plen = bs - divmod(len(plaintext),bs)[1]
padding = [plen]*plen
padding = pack('b'*plen, *padding)
msg = iv + cipher.encrypt(plaintext + padding)

key = b'-8B key-'
nonce = b'0101010101010101'
ctr = Counter.new(DES.block_size*8/2, prefix=nonce)
cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
plaintext = b'We are no longer the knights who say ni!'
msg = nonce + cipher.encrypt(plaintext)

key = b'Super secret key'
cipher = XOR.new(key)
plaintext = b'Encrypt me'
msg = cipher.encrypt(plaintext)
