import argparse
import logging
from os import path


class Conf:

    directories = []
    exclude = []

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
            help='Exclude specific plugin',
            metavar='<plugin-name>', nargs='+')
        args = self.parser.parse_args()
        if args.plug_dir:
            for arg in args.plug_dir:
                if path.isdir(arg):
                    self.directories.append(arg)
                else:
                    logging.warn('"' + arg + '" in not dir!')
        self.exclude = args.exc_plug
