#!/usr/bin/env python
"""Temporary clean manage.py replacement.

The repo's `manage.py` currently contains stray Markdown fences (```), which
causes SyntaxError. Use this file to run Django management commands.
"""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapi.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
