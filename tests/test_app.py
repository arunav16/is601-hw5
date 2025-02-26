"""
Tests for the REPL application and its plugin commands.
"""

import pytest
import pkgutil
import importlib
from app import App
from app.commands import CommandHandler

from app.plugins.greet import GreetCommand
from app.plugins.add import AddCommand
from app.plugins.subtract import SubtractCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.plugins.goodbye import GoodbyeCommand
from app.plugins.exit import ExitCommand

# -------------------------------
# Unit Tests for Individual Command Plugins
# -------------------------------

def test_greet_command():
    """Test that GreetCommand returns the expected greeting."""
    cmd = GreetCommand()
    result = cmd.execute("")
    assert result == "Hello, world!", "GreetCommand should return 'Hello, world!'"

def test_add_usage():
    """Test that AddCommand returns a usage message when not given exactly two arguments."""
    cmd = AddCommand()
    result = cmd.execute("5")
    assert result == "Usage: add <num1> <num2>"

def test_add_command_valid():
    """Test AddCommand with valid inputs."""
    cmd = AddCommand()
    result = cmd.execute("5 3")
    expected = "The result of 5.0 add 3.0 is equal to 8.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_add_command_invalid():
    """Test AddCommand with invalid input."""
    cmd = AddCommand()
    result = cmd.execute("5 a")
    assert "Invalid number input" in result, "AddCommand should indicate an invalid number input"

def test_subtract_command():
    """Test SubtractCommand with valid inputs."""
    cmd = SubtractCommand()
    result = cmd.execute("10 2")
    expected = "The result of 10.0 subtract 2.0 is equal to 8.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_subtract_usage():
    """
    Test that SubtractCommand returns a usage message if the wrong number of arguments is provided.
    """
    cmd = SubtractCommand()
    result = cmd.execute("10")
    assert result == "Usage: subtract <num1> <num2>"

def test_subtract_invalid_input():
    """
    Test that SubtractCommand returns an error message if a token is not a valid number.
    """
    cmd = SubtractCommand()
    result = cmd.execute("10 a")
    assert "Invalid number input" in result

def test_subtract_valid():
    """
    Test that SubtractCommand returns the correct subtraction result for valid input.
    """
    cmd = SubtractCommand()
    result = cmd.execute("10 2")
    expected = "The result of 10.0 subtract 2.0 is equal to 8.0"
    assert result == expected

def test_multiply_command():
    """Test MultiplyCommand with valid inputs."""
    cmd = MultiplyCommand()
    result = cmd.execute("4 5")
    expected = "The result of 4.0 multiply 5.0 is equal to 20.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_multiply_usage():
    """
    Test that MultiplyCommand returns a usage message if the wrong number of arguments is provided.
    """
    cmd = MultiplyCommand()
    result = cmd.execute("4")
    assert result == "Usage: multiply <num1> <num2>"

def test_multiply_invalid_input():
    """
    Test that MultiplyCommand returns an error message if a token is not a valid number.
    """
    cmd = MultiplyCommand()
    result = cmd.execute("4 b")
    assert "Invalid number input" in result

def test_multiply_valid():
    """
    Test that MultiplyCommand returns the correct multiplication result for valid input.
    """
    cmd = MultiplyCommand()
    result = cmd.execute("4 5")
    expected = "The result of 4.0 multiply 5.0 is equal to 20.0"
    assert result == expected

def test_divide_command_valid():
    """Test DivideCommand with valid inputs."""
    cmd = DivideCommand()
    result = cmd.execute("20 4")
    expected = "The result of 20.0 divide 4.0 is equal to 5.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_divide_usage():
    """Test branch when the wrong number of arguments is provided."""
    cmd = DivideCommand()
    result = cmd.execute("20")
    assert result == "Usage: divide <num1> <num2>"

def test_divide_invalid_input():
    """Test branch when one of the tokens is not a valid number."""
    cmd = DivideCommand()
    result = cmd.execute("20 a")
    assert "Invalid number input" in result

def test_divide_by_zero():
    """Test branch when division by zero is attempted."""
    cmd = DivideCommand()
    result = cmd.execute("10 0")
    assert "Cannot divide by zero" in result

def test_divide_valid():
    """Test branch for valid division."""
    cmd = DivideCommand()
    result = cmd.execute("20 4")
    expected = "The result of 20.0 divide 4.0 is equal to 5.0"
    assert result == expected

def test_divide_command_zero():
    """Test DivideCommand when dividing by zero."""
    cmd = DivideCommand()
    result = cmd.execute("10 0")
    assert "Cannot divide by zero" in result, "DivideCommand should indicate division by zero error"

def test_goodbye_command():
    """Test that GoodbyeCommand returns a farewell message."""
    from app.plugins.goodbye import GoodbyeCommand
    cmd = GoodbyeCommand()
    result = cmd.execute("")
    assert result == "Goodbye!!!", "GoodbyeCommand should return 'Goodbye!'"

def test_exit_command():
    """Test that ExitCommand exits the application."""
    from app.plugins.exit import ExitCommand
    cmd = ExitCommand()
    with pytest.raises(SystemExit) as excinfo:
        cmd.execute("")
    assert "Exiting the application" in str(excinfo.value), "ExitCommand should exit with an appropriate message"

# -------------------------------
# Additional Unit Test for CommandHandler (Unknown Command)
# -------------------------------

def test_execute_unknown_command():
    """Test that CommandHandler returns the proper message for unknown commands."""
    handler = CommandHandler()
    result = handler.execute_command("nonexistent", "some args")
    assert "No such command: nonexistent" in result

# -------------------------------
# Test for Error Handling in load_plugins (Simulated Failure)
# -------------------------------

def test_load_plugins_error(monkeypatch, capsys):
    """
    Simulate a failure during plugin import by monkeypatching pkgutil.iter_modules
    and importlib.import_module to force an exception.
    """
    # Create a dummy iter_modules that returns a plugin name "dummy"
    def dummy_iter_modules(path):
        yield None, "dummy", True
    monkeypatch.setattr(pkgutil, "iter_modules", dummy_iter_modules)
    
    # Monkeypatch import_module to raise an Exception for "dummy"
    def dummy_import_module(module_name):
        raise Exception("dummy error")
    monkeypatch.setattr(importlib, "import_module", dummy_import_module)
    
    app_instance = App()
    commands = app_instance.load_plugins()
    captured = capsys.readouterr().out
    assert "Error importing plugin dummy: dummy error" in captured
    assert "dummy" not in commands

# -------------------------------
# Integration Tests for the REPL via the App Class
# -------------------------------

def test_app_repl(monkeypatch, capsys):
    """
    Simulate a REPL session:
      1. "greet"    -> outputs greeting.
      2. "add 5 3"  -> outputs add result.
      3. "unknown"  -> outputs unknown command message.
      4. "exit"     -> exits the REPL.
    """
    inputs = iter(["greet", "add 5 3", "unknown", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    with pytest.raises(SystemExit):
        App().start()
    output = capsys.readouterr().out
    assert "Hello, world!" in output, "REPL should output the greeting."
    assert "The result of 5.0 add 3.0 is equal to 8.0" in output, "REPL should output the add result."
    assert "No such command: unknown" in output, "REPL should notify about unknown commands."

def test_app_empty_input(monkeypatch, capsys):
    """
    Simulate a REPL session where empty inputs are provided, then a valid command, then exit.
    """
    inputs = iter(["", "   ", "greet", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    with pytest.raises(SystemExit):
        App().start()
    output = capsys.readouterr().out
    assert "Hello, world!" in output, "REPL should eventually output the greeting after empty inputs."

def test_app_immediate_exit(monkeypatch, capsys):
    """
    Simulate a REPL session where the first input is 'exit' to test the immediate exit path.
    """
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    with pytest.raises(SystemExit):
        App().start()
    output = capsys.readouterr().out
    assert "Type 'exit' to exit." in output, "REPL should prompt exit instructions before exiting."
