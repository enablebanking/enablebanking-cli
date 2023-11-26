class BaseCommand:
    def handle(self, args):
        command = getattr(args, self.subparsers.dest)
        if command:
            command_handler = getattr(self, command)
            return command_handler(args)
        self.parser.print_help()
