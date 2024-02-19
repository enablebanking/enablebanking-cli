class BaseCommand:
    def handle(self, args):
        command = getattr(args, self.subparsers.dest).replace("-", "_")
        if command:
            if not hasattr(self, command):
                print(f"Command {command} is not implemented")
                return 1
            command_handler = getattr(self, command)
            return command_handler(args)
        self.parser.print_help()
