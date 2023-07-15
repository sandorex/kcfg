#!/usr/bin/env python3
# kcfg
# Copyright (C) 2023 Aleksandar Radivojevic (@Sandorex)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# --------------------------------------------------------------------------- #
# This file is all at once, API, package, script it should always run in all of
# these conditions without issues!
#
# It should not have any dependencies outside the ones provided by python by
# default
# --------------------------------------------------------------------------- #

import sys
import os
import configparser
import argparse

from typing import Tuple, List

VERSION_TUPLE = (0, 1, 0)
VERSION = str('.'.join(str(x) for x in VERSION_TUPLE))

# these are known files and their path on the the computer
PREDEFINED_FILES = {}

# all of these files are in ~/.config
DOT_CONFIG_FILES = [
    "kdeglobals",
    "kscreenlockerrc",
    "kwinrc",
    "ksplashrc",
    "plasmarc",
    "kdeglobals",
    "Trolltech.conf",
    "breezerc",
    "kwinrc",
    "kdeglobals",
    "kcmfonts",
    "kdeglobals",
    "kcminputrc",
    "klaunchrc",
    "kfontinstuirc",
    "ksplashrc",
    "plasmarc",
    "kwinrc",
    "kglobalshortcutsrc",
    "kscreenlockerrc",
    "kactivitymanagerdrc",
    "kactivitymanagerd-switcher",
    "kactivitymanagerd-statsrc",
    "kactivitymanagerd-pluginsrc",
    "kglobalshortcutsrc",
    "plasma-org.kde.plasma.desktop-appletsrc",
    "kwinrc",
    "kwinrulesrc",
    "kwinrc",
    "khotkeysrc",
    "kglobalshortcutsrc",
    "kded5rc",
    "ksmserverrc",
    "krunnerrc",
    "baloofilerc",
    "plasmanotifyrc",
    "plasma-localerc",
    "ktimezonedrc",
    "kaccessrc",
    "kdeglobals",
    "PlasmaUserFeedback",
    "kcminputrc",
    "kxkbrc",
    "touchpadxlibinputrc",
    "kgammarc",
    "powermanagementprofilesrc",
    "bluedevilglobalrc",
    "kdeconnect",
    "device_automounter_kcmrc",
    "kded5rc",
    "kded_device_automounterrc",
]

# populate the dictionary
for file in DOT_CONFIG_FILES:
    PREDEFINED_FILES[file.lower()] = os.path.join(os.getenv('HOME'), '.config', file)

def write_file(fp, data):
    """Writes data to file as INI

    I think there is no need for any processing, just using bare `configparser`
    """
    parser = configparser.ConfigParser()

    # preserves case
    parser.optionxform = str

    parser.read_dict(data)

    parser.write(fp)

# TODO deal with locking [$i]
# TODO deal with dynamic evaluation [$e]
# read more at https://userbase.kde.org/KDE_System_Administration/Configuration_Files#Example:_Using_[$i]
def read_file(filepath) -> dict:
    """Reads data from KDE INI config file

    There was no need for nay processing as configparser does not care for correctness
    """
    parser = configparser.ConfigParser()

    # preserves the case
    parser.optionxform = str

    with open(filepath, 'r') as f:
        data = f.read()

    parser.read_string(data)

    # return a dict
    return { x: dict(parser.items(x)) for x in parser.sections() }

def parse_path(path: str) -> Tuple[List[str], str]:
    """Parses path for the setting, returns the name of section and optionally file

    Multiple formats
        '[Group 1][Group 2]Key' - formatted same as in the file
        '/Group 1/Group 2/Key' - path without file specified, defaults to 'kdeglobals' but another argument should override it
        'kcminputrc/Group 1/Group 2/Key' - path uses 'kcminputrc' file
    """
    if path.startswith('['):
        # replace all brackets so it matches the other syntax to not duplicate the logic
        path = '/' + path[1:].replace('][', '/').replace(']', '/')

    # remove any duplicate slashes
    while '//' in path:
        path = path.replace('//', '/')

    # leading slashes are useless
    if path.endswith('/'):
        path = path[:-1]

    # path must contain a slash
    if '/' not in path:
        raise RuntimeError(f"Invalid path '{path}'")

    segments = path.split('/')
    if len(segments) == 2 and not segments[1]:
        raise RuntimeError(f"Invalid path '{path}', missing both group and key")

    file = segments.pop(0)

    length = len(segments)
    if length < 2 or length == 2 and not segments[1]:
        raise RuntimeError(f"Invalid path '{path}', missing the key")

    # im stripping the path just in case, this may not be a good idea but eh
    return [x.strip for x in segments], file

def print_configs():
    '''Prints all configs files that are known'''
    print('Config files that are known')
    for k, v in PREDEFINED_FILES.items():
        print('  ' + v)
    print()

def main(raw_args=sys.argv[1:]):
    def make_final_action(fn):
        '''Creates action that runs fn and then quits'''
        class custom_action(argparse.Action):
            def __init__(self, nargs=0, **kw):
                super().__init__(nargs=nargs, **kw)

            def __call__(self, parser, args, values, option_string=None):
                fn()
                parser.exit()

        return custom_action

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='kcfg',
        description=rf"""
Version {VERSION}
For source code go to https://github.com/sandorex/kcfg

Replacement for kwriteconfig5 / kreadconfig5 written in Python
""",
        epilog=r"""

Examples:
    $ kcfg '[Group 1][Group 2]Key'

        Is equivalent to

    $ kreadconfig5 --group 'Group 1' --group 'Group 2' --key 'Key'`

        Which could also be written as

    $ kcfg '/Group 1/Group 2/Key'

        You could also specify a known KDE config file

    $ kcfg 'kcminputrc/Group 1/Group 2/Key' which would use ~/.config/kcminputrc

        Alternatively specify the file directly

    $ kcfg --file ~/.config/kcminputrc '/Group 1/Group 2/Key'
""" + ' \n')
    parser.add_argument('--version', action='version', version=f"%(prog)s {VERSION}")
    parser.add_argument('-q', action='store_true', help='makes the application not write anything, unless any error arises')
    parser.add_argument('--file', type=str, help='file to use for read/write operation, error if path is already specified in the path')
    parser.add_argument('--write', type=str, help='write following value to the path')
    parser.add_argument('-l', '--list-configs', action=make_final_action(print_configs), help='lists all known config files then quits')

    # positional
    parser.add_argument('path', help='path to use for read/write operation')

    args = parser.parse_args(raw_args)
    print(args)

    # parse the path # TODO catch exceptions?
    path, file = parse_path(args.path)
    file_from_path = True

    if file and args.file:
        print("File already provided in path, --file argument is ignored", file=sys.stderr)

    # use argument if not provided in path
    if not file:
        file = args.file
        file_from_path = False

    # no file is provided so default to kdeglobals
    if not file:
        file = PREDEFINED_FILES['kdeglobals'] # TODO make this into a global var

        if not args.q:
            print('No file specified, defaulting to kdeglobals')

    # only expand if inside the path
    if file_from_path:
        file = file.lower()

        # get the actual path of the file if its one of the aliases
        if file in PREDEFINED_FILES:
            file = PREDEFINED_FILES[file]
        else:
            # the file is not known
            print(f"Config file '{file}' is not in the database, please provide a full path using --file argument")
            exit(1)

    # i dont have to check anything about the file, it will be created anyways

    if args.write:
        if not args.q:
            print("Writing '{args.write}' to '{args.path}'")

        from io import StringIO

        data = read_file(file)
        # pretend i wrote to it
        buffer = StringIO()
        write_file(buffer, data)
        print(buffer.getvalue())

    print(file, path)

if __name__ == '__main__':
    main()

