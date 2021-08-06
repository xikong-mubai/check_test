import time
import base64
from dns.resolver import *
import hashlib
from itertools import *

def base32_encode(m):
    u = base64.b32encode(m).decode().replace('=','')
    c = '' ; num = '012345'
    for i in u:
        if str.isdigit(i):
            c += num[int(i)-2]
        else:
            c += i
    return c
def base32_decode(c):
    if len(c)%8 != 0:
        c += (8 - len(c) % 8) * '='
    u = '' ; num = '234567'
    for i in c:
        if str.isdigit(i):
            u += num[int(i)]
        else:
            u += i
    u = base64.b32decode(c)
    return u

class iodine_client():
    def __init__(self,url,pwd):
        self.url = url
        self.pwd = pwd
        self.resolver = Resolver()
        self.handshark()
    
    def handshark(self):
        answer = self.resolver.query('yrb123.'+self.url,'null').response.answer[0]
        print(answer)
        answer = self.handshark_version()
        self.seed = answer[:4]
        self.userid = answer[4]
        answer = self.handshark_login()
        
    
    def handshark_version(self):
        version = b'\x00\x00\x05\x02'
        rand = b'\x00\x00'
        payload = 'v' + base32_encode(version+rand) + '.'
        text = self.resolver.query(payload+self.url,'null').response.answer[0]
        print(text)
        text = text[0].data
        if text[:4] != b'VACK':
            raise Exception('please check handshark_version!')
        return text[4:]

    def handshark_login(self):
        self.login = self.login_calculate()
        

    def login_calculate(self):
        if len(self.pwd) < 32:
            self.pwd += '\x00' * (32 - len(self.pwd))
        self.pwd = self.pwd.encode()
        tmp = '' ; num = 0
        for i in self.pwd:
            tmp += hex(i^self.seed[num])[2:].zfill(2)
            num += 1 ; num %= 4
        tmp_md5 = hashlib.md5(bytes.fromhex(tmp)).hexdigest()
        return tmp_md5

def handshark():
    pass

'''
def iodine_client():
    resolver = dns.resolver.Resolver()
    dnsc = '.b.xibai.xyz'
    try:
        #text = resolver.resolve(dnsc, 10)
        text = resolver.query(dnsc,'null')
    #except NoNameservers:
    #    break
    except:
        return
    if text=="":
        pass
        #
        # break    
        #time.sleep(0.3)
    else:
        print(dir(text.response.answer))
        print(type(text.response.answer))
        for i in text.response.answer:
            print(i)
            print(type(i))
    #buff = buff + text
'''

url = 'b.xibai.xyz'
pwd = '123'
iodinec = iodine_client(url,pwd)
print(iodinec.url)
#while True:
#    stager()