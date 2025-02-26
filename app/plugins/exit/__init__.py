from app.commands import Command
import sys
class ExitCommand(Command):
  def execute(self,args: str) -> str:
      return sys.exit("Exiting the application. Goodbye!")