# Compromising pictures 1

## Description
```
You've managed to intercept an exchange between Wario and Bowser Jr. about compromising photos of Mario.
It seems that Wario wants these photos back so he can steal his place as the hero of the Mushroom Kingdom.
Investigate the exchange to find out what it's all about.
```

## Flag
**`ECTF{iTs_ALMo5t_tH3_END_of_m@rIo}`**

## Resolution
- Find the interesting information hidden in the pcapng file => export http objects => "notsuspicious.jpeg"
- Extract files from image => foremost
- Extract files from zip => foremost exif password image => caesar cipher => zip password => "ciaomario"
- Retrieve flag => "readme" file