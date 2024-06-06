class BaseCommand:
    def handle(self, args):
        command = (lambda c: c.replace("-", "_") if c else None)(
            getattr(args, self.subparsers.dest)
        )
        if command:
            if not hasattr(self, command):
                print(f"Command {command} is not implemented")
                return 1
            command_handler = getattr(self, command)
            return command_handler(args)
        self.parser.print_help()
