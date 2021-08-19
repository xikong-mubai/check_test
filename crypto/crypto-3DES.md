# 3DES

3DES算法的提出主要是为了弥补DES算法密钥空间太小的缺陷，相当于连续进行三次DES加密。

## 加密算法

key长度为24字节时：

```c++
VOID 3DES(BYTE DoubleKeyStr[24]， BYTE Data[8]， BYTE Out[8])
{
BYTE Buf1[8]， Buf2[8];
DES (&DoubleKeyStr[0]， Data， Buf1);
UDES(&DoubleKeyStr[8]， Buf1， Buf2);
DES (&DoubleKeyStr[16]， Buf2， Out);
}
```

key长度为16字节时：

```c++
VOID 3DES(BYTE DoubleKeyStr[16]， BYTE Data[8]， BYTE Out[8])
{
BYTE Buf1[8]， Buf2[8];
DES (&DoubleKeyStr[0]， Data， Buf1);
UDES(&DoubleKeyStr[8]， Buf1， Buf2);
DES (&DoubleKeyStr[0]， Buf2， Out);
}
```
