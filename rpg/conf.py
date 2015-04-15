import argparse
import logging
from os import path


class Conf:

    directories = []
    exclude = []
    load_dnf = True

    def parse_cmdline(self):

        self.parser = argparse.ArgumentParser(
            description="Command Line parser",
            prog='Argument Parser Plugin')
        self.parser.add_argument(
            '--plugin-dir', type=str, dest='plug_dir',
            help='Include plugin directory',
            metavar='<dir>', nargs='+')
        self.parser.add_argument(
            '--disable-plugin', type=str, dest='exc_plug',
            help='Exclude specific plugin', default=[],
            metavar='<plugin-name>', nargs='+')
        self.parser.add_argument(
            '--disable-dnf', dest='load_dnf', action='store_false',
            default=True, help='Disable loading DNF sack')
        args = self.parser.parse_args()
        self.load_dnf = args.load_dnf
        if args.plug_dir:
            for arg in args.plug_dir:
                if path.isdir(arg):
                    self.directories.append(arg)
                else:
                    logging.warn('"' + arg + '" in not dir!')
        self.exclude = args.exc_plug
