class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command):
        self.commands[command_name] = command

    def execute_command(self, command_name: str, args: str) -> str:
        command = self.commands.get(command_name)
        if command:
            # If the command is "menu", passing the command dictionary as a second argument.
            if command_name == "menu":
                return command.execute(args, self.commands)
            else:
                return command.execute(args)
        else:
            return f"Unknown command: {command_name}"
