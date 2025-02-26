import pkgutil
import importlib
from app.commands import CommandHandler, Command

class App:
    def __init__(self):  # Constructor
        self.command_handler = CommandHandler()

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'app.plugins'
        # Use pkgutil.iter_modules on the plugins package path (without extra directory operations)
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                except Exception as e:
                    print(f"Error importing plugin {plugin_name}: {e}")
                    continue
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        # Ensure the attribute is a class and a subclass of Command (but not Command itself)
                        if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue
        print("Available commands:", list(self.command_handler.commands.keys()))
        return self.command_handler.commands

    def start(self):
        # Load plugins and then start the REPL
        self.load_plugins()
        print("Type 'exit' to exit.")
        while True:  # REPL: Read, Evaluate, Print, Loop
            command_line = input(">>> ").strip()
            if not command_line:
                continue
            result = self.command_handler.execute_command(command_line)
            if result:
                print(result)
