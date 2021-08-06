import hashlib
import base64
import zlib

def base32_decode(c):
    if len(c)%8 != 0:
        c += (8 - len(c) % 8) * '='
    u = '' ; num = '234567'
    for i in c:
        if str.isdigit(i):
            u += num[int(i)]
        else:
            u += i
    m = base64.b32decode(u.upper())
    return m

def base128_reverse_init(cb128):
    rev128 = [0 for i in range(256)]
    for i in range(128):
        c = cb128[i]
        rev128[ord(c)] = i
    
    return rev128

def base128_decode(c):
    cb128 ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" \
    + "\274\275\276\277" \
    + "\300\301\302\303\304\305\306\307\310\311\312\313\314\315\316\317" \
    + "\320\321\322\323\324\325\326\327\330\331\332\333\334\335\336\337" \
    + "\340\341\342\343\344\345\346\347\350\351\352\353\354\355\356\357" \
    + "\360\361\362\363\364\365\366\367\370\371\372\373\374\375"
    rev128 = base128_reverse_init(cb128)
    num = 0 ; u = b''
    while True:
        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x7f) << 1) | \
                ((rev128[c[num + 1]] & 0x40) >> 6),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x3f) << 2) | \
                ((rev128[c[num + 1]] & 0x60) >> 5),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x1f) << 3) | \
                ((rev128[c[num + 1]] & 0x70) >> 4),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x0f) << 4) | \
                ((rev128[c[num + 1]] & 0x78) >> 3),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x07) << 5) | \
                ((rev128[c[num + 1]] & 0x7c) >> 2),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x03) << 6) | \
                ((rev128[c[num + 1]] & 0x7e) >> 1),1,'big')
        num += 1

        if num + 1 >= len(c):
            break
        u += int.to_bytes(((rev128[c[num]] & 0x01) << 7) | \
                ((rev128[c[num + 1]] & 0x7f)),1,'big')
        num += 1

    return u



seed = b'\x08\x42\x29\x55'
pwd = '123'
if len(pwd) < 32:
    pwd += '\x00' * (32 - len(pwd))
pwd = pwd.encode()
tmp = '' ; num = 0
for i in pwd:
    tmp += hex(i^seed[num])[2:].zfill(2)
    num += 1 ; num %= 4
tmp_md5 = hashlib.md5(bytes.fromhex(tmp)).hexdigest()
print(tmp_md5)

print(base32_decode('ah5wrtn2fac4yuxdpzink0u20l43zsy'))

c_1 = bytes.fromhex('3832ca326449f542de6161bfe0d9fdfd41ca71656c4174d9526ef3e6d4f5fd7a6d4b61767a53684664e06171636be86adc61')
c_2 = bytes.fromhex('3832ca326449f542de6161bfe0d9fdfd41ca71616a4667cbfce671ecd2bdfd7a6d4b61767a56687ad2c661de6371616bdbbe')
temp = base128_decode(c_2)
print(temp.hex(':'))
print(zlib.decompress(temp[:20]+b'\x44\x75\x8b\xef'))
