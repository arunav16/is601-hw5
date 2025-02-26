
## Features
- **Dynamic Plugin Loading:**  
  The App class uses `pkgutil.iter_modules` and `importlib.import_module` to discover and load all command plugins from the `app/plugins` directory automatically.
- **Command Registration:**  
  Each plugin package is expected to define a class that extends the abstract `Command` class. The plugin is registered using its folder name as the command key.
- **Flexible Architecture:**  
  New commands can be added by simply placing a new package in the `app/plugins` folder without modifying any core code.
- **REPL Integration:**  
  The REPL loop reads user input, looks up the command in the dynamically loaded plugins, and executes it.

## Usage
1. **Run the application:**
   python3 main.py
