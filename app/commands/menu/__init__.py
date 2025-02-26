# app/commands/menu/__init__.py
class MenuCommand:
    def execute(self, args: str, command_dict=None) -> str:
        """
        Returns a dynamically generated list of available commands.
        If no command_dict is provided, returns a default message.
        """
        if command_dict is None:
            return "No commands available."
        command_list = ", ".join(sorted(command_dict.keys()))
        return f"Available commands: {command_list}"
