from common import *
v = "0x25"
r = "0xf6a6c7ad385046fc427daae298cdf797d8211f6ca168f0fceebc422635c600f7"
s = "0x1ec43a058eafbee6d33bf4c89aa916db8c4e8eb3df9a300dafdb25aa2b154bf7"
h = "0xf561c5858722e97aaeddc549d579f3c2b999cdb9ffb38b3706a771013f7d71ac"
a = sig_to_addr(h, v, r, s)
print(a)
