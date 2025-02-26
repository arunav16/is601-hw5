from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, args: str) -> str:
        """
        Execute the command with the provided arguments and return a result string.
        """
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_line: str, args: str = "") -> str:
        # Split the input into command name and arguments
        tokens = command_line.split(maxsplit=1)
        cmd_name = tokens[0]
        args = tokens[1] if len(tokens) > 1 else ""
        try:
            return self.commands[cmd_name].execute(args)
        except KeyError:
            return f"No such command: {cmd_name}"
