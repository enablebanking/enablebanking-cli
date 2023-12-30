import os

from argparse import ArgumentParser

from .commands.app import AppCommand
from .commands.auth import AuthCommand


def main():
    parser = ArgumentParser(prog="enablebanking", description="Enable Banking Command-Line Utility")
    parser.add_argument(
        "--cp-domain",
        type=str,
        default="enablebanking.com",
        help="Domain of the Enable Banking Control Panel",
    )
    parser.add_argument(
        "--api-domain",
        type=str,
        default="api.enablebanking.com",
        help="Domain of the Enable Banking API",
    )
    parser.add_argument(
        "--root-path",
        type=str,
        default=os.path.expanduser("~/.enablebanking"),
        help="Root path under which files used by this utility are stored",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    commands = [
        AppCommand(subparsers),
        AuthCommand(subparsers),
    ]

    args = parser.parse_args()

    for command in commands:
        command_prog = command.parser.prog.split(" ", 1)[1]
        if command_prog == args.command:
            command.handle(args)
            break
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
