"""
Todo CLI Application - Main Entry Point

This is the main entry point for the Todo CLI application.
"""
import sys
from cli.menu import run_menu


def main():
    """Main function to run the Todo CLI application."""
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()