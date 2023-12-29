import json
import http.server
import os
import threading

from urllib.parse import parse_qs, urlparse

from commands.base import BaseCommand
from cp_client import CpClient
from cp_store import CpStore


class AuthCallbackRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "OK")
        self.send_header("content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(
            "<html>"
            "<head><title>Enable Banking CLI Authentication Callbakc</title></head>"
            "<body>"
            "<h1>You can close this windows and continue using Enable Banking CLI.</h1>"
            "</body>"
            "</html>",
            "utf-8",
        ))
        self.server.cli_command._callback_query_params = parse_qs(urlparse(self.path).query)          
        self.server.shutdown()

    def send_response(self, code, message=None):
        self.send_response_only(code, message)


class AuthCommand(BaseCommand):
    def __init__(self, parent_subparsers):
        self.parser = parent_subparsers.add_parser("auth", help="Authentication commands")
        self.subparsers = self.parser.add_subparsers(
            title="Authentication Commands",
            dest="auth_command")
        default_parser = self.subparsers.add_parser("default", help="Set default authenticated user")
        default_parser.add_argument("user", type=str, help="User ID")
        list_parser = self.subparsers.add_parser("list", help="List authenticated users")
        login_parser = self.subparsers.add_parser("login", help="Log in as a control panel user")
        login_parser.add_argument("email", type=str, help="User's email")
        login_parser.add_argument(
            "--callback-port",
            type=int,
            default=8888,
            help="Port number of the authentication callback server",
        )
        logout_parser = self.subparsers.add_parser("logout", help="Log out")

    def login(self, args):
        cp_client = CpClient(args.cp_domain)
        response = cp_client.get_oob_confirmation_code(args.email, args.callback_port)
        if response.status != 200:
            print(f"{response.status} response from the relyingparty API: {response.read().decode()}")
            return 1
        print(
            f"A sign-in email with additional instructions was sent to {args.email}. "
            f"Check your email to complete sign-in."
        )
        print("Waiting for authentication completion...")
        http_server = http.server.ThreadingHTTPServer(
            ('localhost', args.callback_port),
            AuthCallbackRequestHandler,
        )
        http_server.cli_command = self
        http_server.serve_forever()
        self._complete_login(args)

    def _complete_login(self, args):
        print("Completing authentication...")
        cp_client = CpClient(args.cp_domain)
        response = cp_client.make_email_link_signin(
            args.email,
            self._callback_query_params["oobCode"][0],
        )
        if response.status != 200:
            print(f"{response.status} response from the relyingparty API: {response.read().decode()}")
            return 2
        auth_data = json.loads(response.read().decode())
        print(f"Authenticated: {json.dumps(auth_data, indent=4)}")
        cp_store = CpStore(args.root_path)
        os.makedirs(cp_store.cp_users_path, exist_ok=True)
        user_filename = f"{auth_data['localId']}.json"
        with open(os.path.join(cp_store.cp_users_path, user_filename), "w") as f:
            f.write(json.dumps(auth_data))
        cp_store.set_default_user_filename(user_filename)
        print("Done!")

    def logout(self, args):
        pass

    def list(self, args):
        cp_store = CpStore(args.root_path)
        users_data = cp_store.load_user_files()
        for user_data in users_data:
            print("*" if user_data["_default"] else " ", user_data["localId"], user_data["email"])

    def default(self, args):
        cp_store = CpStore(args.root_path)
        users_data = cp_store.load_user_files()
        is_user_found = False
        for user_data in users_data:
            if user_data["localId"] == args.user:
                is_user_found = True
                break
        if not is_user_found:
            print(f"User with ID '{args.user}' is not authenticated")
            return 1
        cp_store.set_default_user_filename(f"{args.user}.json")
        print(f"Default user switched to {args.user} ({user_data['email']})")
