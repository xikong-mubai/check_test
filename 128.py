def d128(m):
    cb128 ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" \
    + "\274\275\276\277" \
    + "\300\301\302\303\304\305\306\307\310\311\312\313\314\315\316\317" \
    + "\320\321\322\323\324\325\326\327\330\331\332\333\334\335\336\337" \
    + "\340\341\342\343\344\345\346\347\350\351\352\353\354\355\356\357" \
    + "\360\361\362\363\364\365\366\367\370\371\372\373\374\375"
    print(len(cb128))
    num = 0 ; u=''
    if len(m) % 7 != 0:
        m += (7-len(m))*b'\x00'
    while True:
        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0xfe) >> 1)]
        

        if num + 1>= len(m): 
            break
        u += cb128[((m[num] & 0x01) << 6) |
                    ((m[num + 1] & 0xfc) >> 2)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0x03) << 5) |
                    ((m[num + 1] & 0xf8) >> 3)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0x07) << 4) |
                    ((m[num + 1] & 0xf0) >> 4)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0x0f) << 3) |
                    ((m[num + 1] & 0xe0) >> 5)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0x1f) << 2) |
                    ((m[num + 1] & 0xc0) >> 6)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[((m[num] & 0x3f) << 1) |
                    ((m[num + 1] & 0x80) >> 7)]
        num += 1

        if num + 1>= len(m):
            break
        u += cb128[(m[num] & 0x7f)]
        num += 1
    return u

m = b'x\xdac`h\xbb\x9b7\x80\x00\x088\xad\xff\xff\xfc\xd4\xc2\x01\x05\x9a4N\xda\xb1\xbdtV\xad\xdf\xf9\x91\x89\x00\x15*e`s\xe0\xf1\x00\x00@\x10\xadBo\x00'
print(d128(m).encode())