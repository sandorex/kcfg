# kcfg
Replacement for the awful `kwriteconfig5` (and `kreadconfig5`)

It has path like syntax similar to dconf
```sh
kcfg --file ~/.config/kcminputrc '/Libinput/1241/41119/E-Signal USB Gaming Mouse/PointerAcceleration' --write -0.200
```

Which is much more readable compared to
```sh
# by the way kwriteconfig cant even write negative values and errors out
kwriteconfig5 --file ~/.config/kcminputrc --group 'Libinput' --group '1241' --group '41119' --group 'E-Signal USB Gaming Mouse' --key 'PointerAcceleration' --write ' -0.200'
```

It knows most KDE config files so you do not have to specify the path
```sh
kcfg 'kcminputrc/Libinput/1241/41119/E-Signal USB Gaming Mouse/PointerAcceleration' --write -0.200
```
## Diferences
It writes the value verbatim and reads it verbatim, so special things like `[$i]` `[$e]` or escapes like `\s` are just treated as text\
*This may be implemented in the future or at least show a warning*

## Installation
The whole logic is inside `kcfg.py` which is a self contained python script with no dependencies except `configparser` which is built into python\
Package exists to allow easy installation/updates from pip/pipx

### pip / pipx
I always recommend to use `pipx` to install the package, but if you want to use pip substitute `pipx` with `pip`

If you need it for only one time for example in setup script but have pipx available then you can use
```
pipx run kcfg
```

Or install it with
```
pipx install kcfg
```

You can also install from git
```
pipx install git+https://github.com/sandorex/kcfg
```

Install a specific branch
```
pipx install git+https://github.com/sandorex/kcfg.git@master
```

### Git
You can also add the repository as a submodule, like i do in my dotfiles
```sh
git submodule add https://github.com/sandorex/kcfg

# run it as a package
python3 -m kcfg

# or directly
kcfg/kcfg.py
```

### wget / curl
**Beware this is the least secure option**

```sh
wget https://raw.githubusercontent.com/sandorex/kcfg/master/kcfg.py
kcfg.py
```

```sh
curl https://raw.githubusercontent.com/sandorex/kcfg/master/kcfg.py
kcfg.py
```

