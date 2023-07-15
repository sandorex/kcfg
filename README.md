# kcfg
Replacement for the awful `kwriteconfig5` and `kreadconfig5`[^1]

It has a different syntax but a much improved one, some examples below

```
$ kcfg 'kcminputrc/Libinput/1241/41119/E-Signal USB Gaming Mouse/PointerAcceleration' --write -0.200
```

[^1]: `kwriteconfig5` can't do the one thing it was made for and that is write strings, if you try to write '-0.200' it shits itself...

## Status
The software is almost done but i also plan to write tests to make sure it behaves like it should

## How to use it
The whole logic is inside `kcfg/kcfg.py` and always will be\
This whole python package is just to allow easy installation/updates from pip

You can clone whole repo and run it directly, or as a module `python3 -m kcfg`, you could download it with wget and run it

*Although i would not recommend not updating it right now as it's still untested*

