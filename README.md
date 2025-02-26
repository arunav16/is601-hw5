
## Features
- **Command Pattern:**  
  Each operation (e.g., add, subtract, multiply, divide, greet, exit, goodbye) is implemented as a command class that implements an `execute(args: str) -> str` method.
- **CommandHandler:**  
  A central handler registers all command objects and looks up the appropriate command when a user types its name.
- **REPL Integration:**  
  The App class initializes the CommandHandler, registers commands manually, and starts the REPL loop.
- **Usage Message:**  
  If an unknown command is entered, a friendly error message is returned.

## Usage
1. **Run the application:**
   ```bash
   python3 main.py
