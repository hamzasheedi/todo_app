"""
Tests for the CLI menu system.
"""
import io
import sys
from unittest.mock import patch, MagicMock
from src.cli.menu import run_menu


def test_menu_system():
    """Test the CLI menu system."""
    # Mock user input to simulate menu navigation
    with patch('builtins.input', side_effect=['16', 'quit']) as mock_input:  # Assuming option 16 is to exit
        # Capture the output to verify the menu displays correctly
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            try:
                run_menu()
            except SystemExit:
                # Expected when user selects 'quit'
                pass

            # Check that the menu was displayed
            output = mock_stdout.getvalue()
            assert "Main Menu" in output or "Menu" in output or "--- Main Menu ---" in output
            assert "1." in output  # At least one menu option should be displayed
            assert "16." in output or "Exit" in output  # The quit option should be displayed

    print("CLI menu system test passed!")


def test_menu_option_selection():
    """Test selecting different menu options."""
    # Test that the menu handles invalid input gracefully
    with patch('builtins.input', side_effect=['invalid', '16', 'quit']) as mock_input:
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            try:
                run_menu()
            except SystemExit:
                # Expected when user selects 'quit'
                pass

    print("Menu option selection test passed!")