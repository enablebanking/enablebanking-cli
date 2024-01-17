import json
import os

from enum import Enum

from ..cp_client import CpClient
from ..cp_store import CpStore
from .base import BaseCommand


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
        self.parser.add_argument(
            "-u",
            "--user",
            type=str,
            help="ID of an authenticated user to be used (using default if not provided)",
            required=False,
        )
        self.subparsers = self.parser.add_subparsers(
            title="Application Commands",
            dest="app_command")
        default_parser = self.subparsers.add_parser(
            "default",
            help="Set an application to be used by default",
        )
        default_parser.add_argument("app", type=str, help="Application ID")
        list_parser = self.subparsers.add_parser("list", help="List locally available applications")
        requests_parser = self.subparsers.add_parser(
            "requests",
            help="Fetch logs of requests made by an application",
        )
        requests_parser.add_argument(
            "-a",
            "--app",
            type=str,
            help="Application ID (using default if not provided)",
            required=False,
        )
        requests_parser.add_argument(
            "--account-id",
            type=str,
            help="Filtering requests associated with an account by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--aspsp-country",
            type=str,
            help="Filtering requests by a country (ISO 3166 code)",
            required=False,
        )
        requests_parser.add_argument(
            "--aspsp-name",
            type=str,
            help="Filtering requests by ASPSP name",
            required=False,
        )
        requests_parser.add_argument(
            "--auth-approach",
            type=str,
            help="Filtering requests by an authorization approach",
            required=False,
        )
        requests_parser.add_argument(
            "--auth-method",
            type=str,
            help="Filtering requests by an authorization method",
            required=False,
        )
        requests_parser.add_argument(
            "--authorization-id",
            type=str,
            help="Filtering requests associated with an authorization by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--endpoint-name",
            type=str,
            help="Filtering requests by an endpoint name",
            required=False,
        )
        requests_parser.add_argument(
            "--payment-id",
            type=str,
            help="Filtering requests associated with a payment by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--psu-type",
            type=str,
            help="Filtering requests by PSU type",
            required=False,
        )
        requests_parser.add_argument(
            "--response-code",
            type=str,
            help="Filtering requests by a response code",
            required=False,
        )
        requests_parser.add_argument(
            "--session-id",
            type=str,
            help="Filtering requests associated with a session by its ID",
            required=False,
        )
        requests_parser.add_argument(
            "--session-status",
            type=str,
            help="Filtering requests by a session status",
            required=False,
        )
        register_parser = self.subparsers.add_parser("register", help="Register an application")
        register_parser.add_argument(
            "-n",
            "--name",
            type=str,
            help="Name of the application being registered",
            required=True,
        )
        register_parser.add_argument(
            "-d",
            "--description",
            type=str,
            help="Description of the application being registered",
            required=False,
        )
        register_parser.add_argument(
            "-e",
            "--environment",
            type=Environment,
            choices=[*Environment],
            help=f"Environment, which the application will use",
            required=True,
        )
        register_parser.add_argument(
            "-r",
            "--redirect-urls",
            type=str,
            nargs="+",
            help=f"Redirect URL(s) allowed for the application",
            required=True,
        )
        register_parser.add_argument(
            "-c",
            "--cert-path",
            type=str,
            help=f"Path to a certificate or a public key of the application",
            required=True,
        )
        register_parser.add_argument(
            "-k",
            "--key-path",
            type=str,
            help=f"Path to a private key of the application (used to generate or verify public key)",
            required=False,
        )
        self.subparsers.add_parser("share", help="Share an application")

    def register(self, args):
        print("Registering an application...")
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_user_path(args.user))
        with open(args.cert_path, "r") as f:
            cert_content = f.read()
        response = cp_client.register_application({
            "name": args.name,
            "description": args.description,
            "certificate": cert_content,
            "environment": args.environment,
            "redirect_urls": args.redirect_urls,
        })
        if response.status != 200:
            print(f"{response.status} response from the applications API: {response.read().decode()}")
            return 1
        response_data = json.loads(response.read().decode())
        print(f"The application is registered under ID {response_data['app_id']}")
        cp_store = CpStore(args.root_path)
        os.makedirs(cp_store.cp_apps_path, exist_ok=True)
        app_filename = cp_store.get_app_filename(response_data["app_id"])
        with open(os.path.join(cp_store.cp_apps_path, app_filename), "w") as f:
            f.write(json.dumps({
                "kid": response_data["app_id"],
                "name": args.name,
                "description": args.description,
                "certificate": cert_content,
                "key_path": args.key_path,
                "environment": args.environment,
                "redirect_urls": args.redirect_urls,
            }, indent=4))
        cp_store.set_default_app_filename(app_filename)
        print("Done!")

    def list(self, args):
        cp_store = CpStore(args.root_path)
        apps_data = cp_store.load_app_files()
        for app_data in apps_data:
            print("*" if app_data["_default"] else " ", app_data["kid"], app_data["name"])

    def default(self, args):
        cp_store = CpStore(args.root_path)
        apps_data = cp_store.load_app_files()
        is_app_found = False
        for app_data in apps_data:
            if app_data["kid"] == args.app:
                is_app_found = True
                break
        if not is_app_found:
            print(f"Application with ID '{args.app}' is not available")
            return 1
        cp_store.set_default_app_filename(cp_store.get_app_filename(args.app))
        print(f"Default application switched to {args.app} ({app_data['name']})")

    def requests(self, args):
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_user_path(args.user))
        app_id = args.app if args.app is not None else cp_store.load_app_file()["kid"]
        print("Fetching requests...")
        response = cp_client.fetch_requests(
            app_id,
            account_id=args.account_id,
            aspsp_country=args.aspsp_country,
            aspsp_name=args.aspsp_name,
            auth_approach=args.auth_approach,
            auth_method=args.auth_method,
            authorization_id=args.authorization_id,
            endpoint_name=args.endpoint_name,
            payment_id=args.payment_id,
            psu_type=args.psu_type,
            response_code=args.response_code,
            session_id=args.session_id,
            session_status=args.session_status,
        )
        if response.status != 200:
            print(f"{response.status} response from the requests API: {response.read().decode()}")
            return 1
        response_data = json.loads(response.read().decode())
        requests = response_data["requests"]
        print(f"Fetched {len(requests)} requests" + (":" if len(requests) else "."))
        print(json.dumps(requests, indent=4))
        print("Done!")
