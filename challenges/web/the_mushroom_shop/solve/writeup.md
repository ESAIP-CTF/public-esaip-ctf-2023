# The Mushroom Shop

## Description
```
Mario has decided to create his online mushrooms store.
Before the official launch he would like to make sure that his website is secure.
Help Mario by checking his online store for any remaining vulnerabilities that could lead to an information disclosure.
```

## Flag
**`ECTF{taK3_c4re_0F_Y0Ur_PRIV4t3_REPos}`**

## Resolution
- Find the vulnerability => LFI on the "page" parameter (bypass "../" with "..././")
- Read generic files such as "/etc/passwd" => presence of a user "mario"
- Look at what is in "/home/mario" => interesting commands in the ".bash_history" or ".sh_history"
- Clone the Github repo => need to have the private key of mario to clone it => "..././..././..././..././home/mario/.ssh/id_rsa" => read the flag