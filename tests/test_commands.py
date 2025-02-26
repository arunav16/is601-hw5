import pytest
from app import App
from app.commands.greet import GreetCommand
from app.commands.goodbye import GoodbyeCommand
from app.commands.add import AddCommand
from app.commands.subtract import SubtractCommand
from app.commands.multiply import MultiplyCommand
from app.commands.divide import DivideCommand
from app.commands.menu import MenuCommand
from app.commands.exit import ExitCommand

def test_greet_command():
    command = GreetCommand()
    result = command.execute("")
    # Adjust the expected string to match your implementation.
    assert result == "Hello, world!", "GreetCommand should return 'Hello, world!'"

def test_goodbye_command():
    command = GoodbyeCommand()
    result = command.execute("")
    # Adjust the expected string to match your implementation.
    assert result == "Goodbye!!!", "GoodbyeCommand should return 'Goodbye!'"

def test_add_command():
    command = AddCommand()
    result = command.execute("5 3")
    expected = "The result of 5.0 add 3.0 is equal to 8.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_subtract_command():
    command = SubtractCommand()
    result = command.execute("10 2")
    expected = "The result of 10.0 subtract 2.0 is equal to 8.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_multiply_command():
    command = MultiplyCommand()
    result = command.execute("4 5")
    expected = "The result of 4.0 multiply 5.0 is equal to 20.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_divide_command():
    command = DivideCommand()
    result = command.execute("20 4")
    expected = "The result of 20.0 divide 4.0 is equal to 5.0"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_divide_by_zero():
    command = DivideCommand()
    result = command.execute("1 0")
    expected = "An error occurred: Cannot divide by zero"
    assert result == expected, f"Expected: {expected}, got: {result}"

def test_menu_command():
    command = MenuCommand()
    # Create a dummy commands dictionary with sample command names.
    dummy_commands = {
        "greet": None,
        "add": None,
        "subtract": None,
        "mul": None,
        "divide": None,
        "menu": None,
        "exit": None,
        "goodbye": None,
    }
    result = command.execute("", dummy_commands)
    # Check that every command name appears in the menu output.
    for cmd in dummy_commands.keys():
        assert cmd in result, f"Menu output should contain '{cmd}'"

def test_app_greet_command(monkeypatch):
    """Test that the REPL correctly handles the 'greet' command."""
    # Simulate user entering 'greet' then 'exit' to trigger a SystemExit.
    inputs = iter(['greet', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    with pytest.raises(SystemExit):
        app.start()

def test_app_menu_command(monkeypatch):
    """Test that the REPL correctly handles the 'menu' command."""
    # Simulate user entering 'menu' then 'exit'
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    with pytest.raises(SystemExit):
        app.start()
