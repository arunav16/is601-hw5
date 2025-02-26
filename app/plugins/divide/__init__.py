from app.commands import Command
class DivideCommand(Command):
    def execute(self, args):
        """
        Expects a string with two numbers separated by space, e.g. "20 4".
        Returns the result of division.
        """
        tokens = args.split()
        if len(tokens) < 2:
            return "Usage: divide <num1> <num2>"
        try:
            num1 = float(tokens[0])
            num2 = float(tokens[1])
        except ValueError:
            return f"Invalid number input: {tokens[0]} or {tokens[1]} is not a valid number."
        if num2 == 0:
            return "An error occurred: Cannot divide by zero"
        result = num1 / num2
        return f"The result of {num1} divide {num2} is equal to {result}"