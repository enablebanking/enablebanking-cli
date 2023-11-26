import json
import os

from enum import Enum

from commands.base import BaseCommand
from cp_client import CpClient
from cp_store import CpStore


class Environment(str, Enum):
    PRODUCTION = "PRODUCTION"
    SANDBOX = "SANDBOX"

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class AppCommand(BaseCommand):
    def __init__(self, parent_subparsers):
        self.parser = parent_subparsers.add_parser("app", help="Application commands")
        self.subparsers = self.parser.add_subparsers(
            title="Application Commands",
            dest="app_command")
        register_parser = self.subparsers.add_parser("register", help="Register an application")
        register_parser.add_argument(
            "-n",
            "--name",
            type=str,
            help="Name of the application being registered",
            required=True,
        )
        register_parser.add_argument(
            "-e",
            "--environment",
            type=Environment,
            choices=[*Environment],
            help=f"Environment, which the application will use",
            required=True,
        )
        self.subparsers.add_parser("share", help="Share an application")

    def register(self, args):
        print("Registering an application...")
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_default_user_path())
        response = cp_client.register_application({
            "name": args.name,
            "certificate": "",
            "environment": args.environment,
            "redirect_urls": ["http://localhost:8888/auth_cb"],
        })
        if response.status != 200:
            print(f"{response.status} response from the applications API: {response.read().decode()}")
            return 1
        print(response.read().decode())
