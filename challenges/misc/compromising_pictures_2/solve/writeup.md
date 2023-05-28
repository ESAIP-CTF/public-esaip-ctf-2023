# Compromising pictures 2

## Description
```
You have heard that an exchange is going to take place between Wario and Bowser Jr.
It seems that the location is written in the corrupted picture that was attached to the message from Bowser Jr.
Your friend and cybersecurity expert Toad thinks that the problem comes from the header of the picture.
Find the name of the location of the exchange in the corrupted photo.
```

## Flag
**`ECTF{mO0_MOO_meaDOW5}`**

## Resolution
- Find the right jpg header => https://en.wikipedia.org/wiki/List_of_file_signatures + test the headers => "FF D8 FF E1 ???? 45 78 69 66 00 00"
- Bruteforce the remaining bytes ("?? ??") => Python code => "0F 0C"
- Get the flag => look at the image