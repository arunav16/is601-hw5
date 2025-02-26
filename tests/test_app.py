import pytest
from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on the 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    # Ensure that SystemExit is raised.
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test that the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    app = App()
    with pytest.raises(SystemExit):
        app.start()
    
    # Verify that the output contains the unknown command message.
    captured = capfd.readouterr()
    assert "Unknown command: unknown_command" in captured.out
