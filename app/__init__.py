import pkgutil
import importlib
import sys
from app.commands import CommandHandler, Command
import os
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)
    
    #def __init__(self):  # Constructor
        #self.command_handler = CommandHandler()

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
                    logging.error(f"Error importing plugin {plugin_name}: {e}")
                    continue
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        # Ensure the attribute is a class and a subclass of Command (but not Command itself)
                        if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                            self.command_handler.register_command(plugin_name, item())
                            logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")
                    except TypeError:
                        continue
        print("Available commands:", list(self.command_handler.commands.keys()))
        return self.command_handler.commands

    def start(self):
      self.load_plugins()
      print("Type 'exit' to exit.")
      logging.info("Application started. Type 'exit' to exit.")
      try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    logging.info("Application exit.")
                    sys.exit(0)  # Use sys.exit(0) for a clean exit, indicating success.
                try:
                    if not cmd_input:
                      continue
                    result = self.command_handler.execute_command(cmd_input)
                    if result:
                        print(result)
                except KeyError:  # Assuming execute_command raises KeyError for unknown commands
                    logging.error(f"Unknown command: {cmd_input}")
                    sys.exit(1)  # Use a non-zero exit code to indicate failure or incorrect command.
      except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0)  # Assuming a KeyboardInterrupt should also result in a clean exit.
      finally:
            logging.info("Application shutdown.")

if __name__ == "__main__":
     app = App()
     app.start()