import sys
class ExitCommand:
  def execute(self,args: str) -> str:
      return sys.exit("Exiting the application. Goodbye!")
