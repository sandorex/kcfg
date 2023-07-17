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
"""Tool to read and write KDE INI config files, replaces kwriteconfig5 / kreadconfig5
"""

__version__ = '0.1.1'

import sys
import os
import configparser
import argparse
from io import StringIO

from typing import Tuple, List, Optional

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

# default file used if no file is specified
DEFAULT_FILE = PREDEFINED_FILES['kdeglobals']

def _parse_path(path: str) -> Tuple[List[str], str]:
    """Parses path for the setting, returns the name of section and optionally file

    Parses it like a path:
        '/Group 1/Group 2/Key' - path without file specified
        'kcminputrc/Group 1/Group 2/Key' - path with file alias specified
    """
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
    return [x.strip() for x in segments], file

def _print_configs():
    '''Prints all configs files that are known'''
    print('Config files that are known')
    for k, v in PREDEFINED_FILES.items():
        print('  ' + v)
    print()
    print('If you feel like any are missing or should be removed make an issue at:')
    print('  https://github.com/sandorex/kcfg')
    print()

def _print_version_api():
    '''Prints the version as a number for easy comparison in shell scripts'''
    print(__version__.replace('.', ''))

def _create_parser():
    '''Function that builds the parser'''

    def make_final_action(fn):
        '''Creates argparse action that runs fn and then quits'''
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
        description=r"""
Licensed under GPLv3
For source code go to https://github.com/sandorex/kcfg

Replacement for kwriteconfig5 / kreadconfig5 written in Python
""",
        epilog=r"""

Examples:
    $ kcfg '/Group 1/Group 2/Key'

        Which is equivalent to

    $ kreadconfig5 --group 'Group 1' --group 'Group 2' --key 'Key'`

        You could also specify a config alias like

    $ kcfg 'kcminputrc/Group 1/Group 2/Key' which would use ~/.config/kcminputrc

        Alternatively specify the file directly

    $ kcfg --file ~/.config/kcminputrc '/Group 1/Group 2/Key'

        To write to a file just add --write value

    $ kcfg --file ~/.config/kcminputrc '/Group 1/Group 2/Key' --write true
""" + ' \n')
    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('--version-api', action=make_final_action(_print_version_api), help='prints program version as an integer for ease of use in shell scripts')
    parser.add_argument('-q', '--quiet', action='store_true', help='makes the application not write anything, unless any error arises')
    parser.add_argument('--file', type=str, help='file to use for read/write operation, error if path is already specified in the path')
    parser.add_argument('--write', type=str, help='write following value VERBATIM')
    parser.add_argument('--delete', action='store_true', help='delete the key value if it exists')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='prints the result instead of writing to the file, does nothing when reading')
    parser.add_argument('-l', '--list-configs', action=make_final_action(_print_configs), help='lists all known config files then quits')

    # positional
    parser.add_argument('path', help='path to use for read/write operation')

    return parser

def main(raw_args=sys.argv[1:]):
    parser = _create_parser()
    args = parser.parse_args(raw_args)

    def print_loud(*argss, **kwargs):
        '''Prints only if quiet is not enabled'''
        if not args.quiet:
            print(*argss, **kwargs)

    def print_err(*args, **kwargs):
        '''Prints error message to stderr'''
        print('[Error]', *args, **kwargs, file=sys.stderr)

    if args.dry_run:
        print_loud("Dry run enabled")

    # parse the path
    path, file = _parse_path(args.path)
    file_from_path = True

    if file and args.file:
        print_err("File already provided in path, --file argument is ignored")

    if args.delete and args.write:
        print_err("Argument --delete and --write cannot be used together")
        exit(1)

    # use argument if not provided in path
    if not file:
        file = args.file
        file_from_path = False

    # no file is provided so default it is
    if not file:
        file = DEFAULT_FILE

        print_loud('No file specified, defaulting to kdeglobals')

    # only expand if file is specified inside the path
    if file_from_path:
        # lowercase cause some files are just weirdly cased
        file = file.lower()
        if file in PREDEFINED_FILES:
            file = PREDEFINED_FILES[file]
        else:
            # the file is not known
            print_err(f"Config file '{file}' is not in the database, please provide a full path using --file argument")
            exit(1)

    key = path.pop()
    section = ']['.join(path)

    # the file may not exist
    try:
        data = read_file(file)
    except FileNotFoundError:
        data = {}

    if args.delete:
        print_loud(f"Deleting '{args.path}' in '{file}'")

        old_value = delete_section_key(data, section, key)
        if old_value is None:
            # exit as there is no need to write to file as either the section
            # or the key do not exist
            exit(0)

        print_loud(f"Value was '{old_value}'")

        if not args.dry_run:
            with open(file, 'w') as fp:
                write_file(fp, data)
        else:
            buffer = StringIO()
            write_file(buffer, data)
            print(buffer.getvalue())
    elif args.write is not None:
        print_loud(f"Setting '{args.path}' to '{args.write}' in '{file}'")

        old_value = set_section_key(data, section, key, args.write)
        if old_value is not None:
            print_loud(f"Value was '{old_value}'")

        if not args.dry_run:
            with open(file, 'w') as fp:
                write_file(fp, data)
        else:
            buffer = StringIO()
            write_file(buffer, data)
            print(buffer.getvalue())
    else:
        if not data:
            print_loud(f"File '{file}' is empty or does not exist")

            exit(0)

        if read_section_key(data, section, key) is None:
            print_loud(f"Path '{args.path}' not found in '{file}'")

## API ##

def write_file(fp, data):
    """Writes data to file as INI

    I think there is no need for any processing, just using bare `configparser`
    """
    parser = configparser.ConfigParser()

    # preserves case
    parser.optionxform = str

    parser.read_dict(data)

    # kwriteconfig5 does not add spaces around delimiters
    parser.write(fp, space_around_delimiters=False)

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

def delete_section_key(data, section, key) -> Optional[str]:
    """Deletes the key in section of data, returns original value if it exists
    otherwise None"""
    try:
        old = data[section][key]
        del data[section][key]
        return old
    except KeyError:
        return None

def set_section_key(data, section, key, value) -> Optional[str]:
    """Sets the key in section of data to value, if it exists already the
    original value is returned otherwise None
    """
    try:
        old = data[section][key]
        data[section][key] = value
        return old
    except KeyError:
        # the section does not exist so create it
        data[section] = { key: value }
        return None

def read_section_key(data, section, key, default=None) -> Optional[str]:
    """Reads key from section of data, if the key (or section) does not exist
    then default is return"""
    try:
        return data[section][key]
    except KeyError:
        return default

if __name__ == '__main__':
    main()

