#!/usr/bin/env python
import os
import sys

# Adding py librairy to sys path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "py"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "py.psionic_storm.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
