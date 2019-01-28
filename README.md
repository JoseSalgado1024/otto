Otto
---

This project is a few hours python 3 experiment. I try to build a keygen option to be used with aircrack.

ToC
[Requirements](#requirements)
[Installation](#installation)
[Usage](#usage)
[Issues](#issues)

# Requirements


# Installation
Cause is pure python3 script and also it is built around builtins python3 libraries, install it is very easy and simple.

```bash 
# Clone repository
git clone https://github.com/JoseSalgado1024/otto.git
```

# Usage
Demo:

    python otto/main.py --randomize --uppercase --whitespace

**Output**

    KZWtvjCyaDdKBeGl
    Yjw RFgbhcWptCo 
    KsclmñKFQXvzRsnk
    JQLWCAbwarñtsrHf
    ygNxFMAgQOBKHUJr
    CcÑRsSqMhDHzmjTh
    rFrtLuzPyVALtBHj
    cgrcHgDCKMNRQpEU
    HnÑHFPrxUcEsogBA
    PxaVWNDgvFañd WÑ

Arguments:

+ `-r` | `--randomize`: Random Method. If randomize flag is not present, Combinations method it'll be selected. 
+ `-d` | `--dictionary`: Custom dictionary. By default `aabcdefghijklmnñopqrstuvwxyz`.
+ `-a` | `--amount`: How many keys do you wanna generate. By default `10`.
+ `-u` | `--uppercase`: Include upper case chars. By default `False`.
+ `-w` | `--whitespace`: Include white spaces into dictionary. No takes effect with user provided dictionaries. By default `False`.
+ `-n` | `--numbers`: Include numbers in the default dictionary. No takes effect with user provided dictionaries. by default `False`.
+ `-l` | `--length`: Key length. By default `10`.

# Issues
If you found any error or something that not seems ok at all, please submit all [issues](https://github.com/JoseSalgado1024/otto/issues/new?title=i%20found%20some%20error%20in...) that you want!