"""This module provides coloured output support for argparse.

It defines:
- COLOUR_DICT: plain (non-bold) ANSI colour codes
- ColourHelpFormatter: HelpFormatter that injects colour into usage, section
  headings and option strings
- ColoredArgParser: ArgumentParser that defaults to using the coloured
  formatter and prints coloured errors/usage.
"""

import re
import sys
import argparse
from gettext import gettext
from typing import Optional

# ANSI colour codes
COLOUR_DICT = {
    "RED": "31",
    "GREEN": "32",
    "YELLOW": "33",
    "BLUE": "34",
    "MAGENTA": "35",
    "CYAN": "36",
    "WHITE": "37",
    "GREY": "90",
    "SAGE":  "38;5;108",
    "ROSE":  "38;5;167",
    "LILAC": "38;5;141",
}


def _colourise(text: str, colour_code: Optional[str]) -> str:
    """Return *text* wrapped in ANSI colour sequence if *colour_code* given."""
    if colour_code is None:
        return text
    return f"\x1b[{colour_code}m{text}\x1b[0m"


class ColourHelpFormatter(argparse.HelpFormatter):
    """HelpFormatter that adds colour to key parts of the help output."""

    def start_section(self, heading: str) -> None:  # type: ignore[override]
        # Section headings such as "optional arguments:" or "positional arguments:"
        coloured_heading = _colourise(heading, COLOUR_DICT["GREEN"])
        super().start_section(coloured_heading)

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = _colourise('usage:', COLOUR_DICT['GREEN']) + ' '
        super().add_usage(usage, actions, groups, prefix)

    # Colour option strings ("-m", "--model")
    def _format_action_invocation(self, action: argparse.Action) -> str:  # noqa: N802
        # Positional arguments – keep default behaviour
        if not action.option_strings:
            return super()._format_action_invocation(action)

        # Colour each option flag
        parts = [_colourise(flag, COLOUR_DICT["CYAN"]) for flag in action.option_strings]

        # Append metavar if the option expects an argument
        if action.nargs != 0:
            metavar = self._format_args(action, action.dest.upper())
            parts[-1] = f"{parts[-1]} {metavar}"
        return ", ".join(parts)

    def _format_args(self, action, default_metavar):
        # Let the base class build whatever text it wants…
        text = super()._format_args(action, default_metavar)
        # …then wrap it in colour
        return _colourise(text, COLOUR_DICT["GREY"])

    # Colour default values in help text
    def _get_help_string(self, action: argparse.Action) -> str:  # noqa: N802
        """Return help string with coloured default values (if any)."""
        help_text = super()._get_help_string(action)
        # Regex to find '(default: something)' pattern
        match = re.search(r"\(default: ([^)]+)\)", help_text)
        if match:
            value = match.group(1)
            coloured_value = _colourise(value, COLOUR_DICT["YELLOW"])
            help_text = help_text.replace(match.group(0), f"(default: {coloured_value})")
        return help_text


class ColoredArgParser(argparse.ArgumentParser):
    """ArgumentParser with coloured help/usage/error output."""

    colour_dict = COLOUR_DICT  # preserve attribute name used elsewhere

    def __init__(self, *args, **kwargs):
        # Default to our colour help formatter if caller didn't specify one
        kwargs.setdefault("formatter_class", ColourHelpFormatter)
        super().__init__(*args, **kwargs)

    # The default ArgumentParser implementations of print_help/usage already
    # call the formatter, so we just pass-through here to keep compatibility
    def print_usage(self, file=None):  # type: ignore[override]
        if file is None:
            file = sys.stdout
        usage = self.format_usage()
        usage = usage.replace('usage:', _colourise('usage:', COLOUR_DICT['RED']), 1)
        self._print_message(usage, file)

    def print_help(self, file=None):  # type: ignore[override]
        if file is None:
            file = sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message: str, file=None):  # type: ignore[override]
        if message:
            if file is None:
                file = sys.stderr
            file.write(message)

    # Ensure error and exit messages are coloured red
    def exit(self, status: int = 0, message: Optional[str] = None):  # type: ignore[override]
        if message:
            self._print_message(_colourise(message, COLOUR_DICT["RED"]), sys.stderr)
        sys.exit(status)

    def error(self, message):  # type: ignore[override]
        self.print_usage(sys.stderr)
        args = {"prog": self.prog, "message": message}
        self.exit(2, gettext("%(prog)s: error: %(message)s\n") % args)
