from app.commands import Command
class GoodbyeCommand(Command):
    def execute(self, args: str) -> str:
    # The greet command ignores any arguments and returns a greeting message.
      return "Goodbye!!!"