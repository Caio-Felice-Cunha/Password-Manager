"""Root entry point for the Password Manager CLI.

Run from the repository root:

    python main.py

This wrapper exists so the app can be launched without worrying about the
working directory. The interactive menu lives in templates/template.py.
"""
from templates.template import main

if __name__ == "__main__":
    main()
