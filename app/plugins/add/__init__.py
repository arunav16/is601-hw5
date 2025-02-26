from app.commands import Command
class AddCommand(Command):
    def execute(self, args):
        """
        Expects a string with two numbers separated by space, e.g. "5 3".
        Returns the result of addition.
        """
        tokens = args.split()
        if len(tokens) < 2:
            return "Usage: add <num1> <num2>"
        try:
            num1 = float(tokens[0])
            num2 = float(tokens[1])
        except ValueError:
            return f"Invalid number input: {tokens[0]} or {tokens[1]} is not a valid number."
        result = num1 + num2
        return f"The result of {num1} add {num2} is equal to {result}"