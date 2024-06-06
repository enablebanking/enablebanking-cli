import json

from datetime import datetime

from ..cp_client import CpClient
from ..cp_store import CpStore
from .base import BaseCommand


class AspspCommand(BaseCommand):
    def __init__(self, parent_subparsers):
        self.parser = parent_subparsers.add_parser("aspsp", help="ASPSP commands")
        self.parser.add_argument(
            "-u",
            "--user",
            type=str,
            help="ID of an authenticated user to be used (using default if not provided)",
            required=False,
        )
        self.subparsers = self.parser.add_subparsers(
            title="ASPSP Commands",
            dest="aspsp_command")
        status_parser = self.subparsers.add_parser(
            "status",
            help="Retrieves ASPSP statuses",
        )
        status_parser.add_argument(
            "-o",
            "--outfile",
            nargs="?",
            const="default",
            type=str,
            help="Outputing status to a file instead of printing to console",
            required=False,
        )

    def status(self, args):
        cp_store = CpStore(args.root_path)
        cp_client = CpClient(args.cp_domain, cp_store.get_user_path(args.user))
        print("Fetching today stats...")
        response = cp_client.fetch_today_stats()
        if response.status != 200:
            print(f"{response.status} response from the today stats API: {response.read().decode()}")
            return 1
        response_data = json.loads(response.read().decode())
        aspsp_statuses = sorted(response_data, key=lambda e: e['country'] + e['brand'] + e['psu_type'])
        if args.outfile is None:
            country = None
            for aspsp_status in aspsp_statuses:
                if country is None or country != aspsp_status['country']:
                    country=aspsp_status['country']
                    print(country)
                print(f"  {aspsp_status['brand']} ({aspsp_status['psu_type']}) {' '*(70-len(aspsp_status['brand']))} {aspsp_status['status']}")
        else:
            if args.outfile == "default":
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"aspsp-statuses-{now}.json"
            else:
                filename = args.outfile
            print(f"Saving ASPSP statuses to {filename}...")
            with open(filename, "w") as f:
                f.write(json.dumps(aspsp_statuses, indent=4))
