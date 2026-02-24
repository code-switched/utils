"""Recursively rename files by moving timestamp from filename to description."""

import re
import sys
from pathlib import Path
from typing import List, Tuple


# ANSI color escape codes
ANSI_RED, ANSI_GREEN, ANSI_YELLOW, ANSI_BLUE = '\033[31m', '\033[32m', '\033[33m', '\033[34m'
ANSI_MAGENTA, ANSI_CYAN, ANSI_GREY, ANSI_RESET = '\033[35m', '\033[36m', '\033[90m', '\033[0m'

# The regex handles two timestamp formats:
# 1. Standard: YYYY-MM-DD-HH-MM-SS-AM|PM  (e.g., 2025-10-09-21-15-39-PM)
# 2. Edge case: YYYY-MM-DD_-_HH-MM-SS(-AM|PM)  (e.g., 2025-05-29_-_19-29-55)
REGEX_PR = r"(.+)-(\d{4}-\d+-\d+(?:-\d+-\d+-\d+-\w+|_-_\d+-\d+-\d+(?:-\w+)?))"
REPLACE_WITH = r"\2-\1"


def find_matching_files(root_dir: Path) -> List[Tuple[Path, str]]:
    """Find all files matching the timestamp pattern.
    
    Returns:
        List of tuples (file_path, new_filename)
    """
    matches = []
    for file_path in root_dir.rglob("*"):
        if file_path.is_file():
            filename = file_path.name
            new_filename = re.sub(REGEX_PR, REPLACE_WITH, filename)

            # Only include files that would actually be renamed
            if new_filename != filename:
                matches.append((file_path, new_filename))

    return matches


def display_dry_run(matches: List[Tuple[Path, str]]) -> None:
    """Display the dry run showing what would be renamed."""
    print("\n" + f"{ANSI_BLUE}{'='*80}{ANSI_RESET}")
    print(f"{ANSI_YELLOW}DRY RUN{ANSI_RESET} - Files that would be renamed:")
    print(f"{ANSI_BLUE}{'='*80}{ANSI_RESET}\n")

    for file_path, new_filename in matches:
        print(f"FROM: {ANSI_RED}{file_path.name}{ANSI_RESET}")
        print(f"  TO: {ANSI_GREEN}{new_filename}{ANSI_RESET}")
        print()

    print(f"\nTotal files to rename: {ANSI_GREEN}{len(matches)}{ANSI_RESET}")


def rename_files(matches: List[Tuple[Path, str]]) -> None:
    """Actually rename the files."""
    print("\n" + f"{ANSI_BLUE}{'='*80}{ANSI_RESET}")
    print(f"{ANSI_MAGENTA}Renaming files...{ANSI_RESET}")
    print(f"{ANSI_BLUE}{'='*80}{ANSI_RESET}\n")

    success_count = 0
    error_count = 0

    for file_path, new_filename in matches:
        try:
            new_path = file_path.parent / new_filename
            file_path.rename(new_path)
            print(f"{ANSI_GREEN}✓{ANSI_RESET} {ANSI_CYAN}{file_path.name}{ANSI_RESET}")
            success_count += 1
        except OSError as e:
            name_part = f"{ANSI_YELLOW}{file_path.name}{ANSI_RESET}"
            err_part = f"{ANSI_RED}{e}{ANSI_RESET}"
            err_msg = f"Error renaming {name_part}: {err_part}"
            print(f"{ANSI_RED}✗{ANSI_RESET} {err_msg}")
            error_count += 1

    print("\n" + f"{ANSI_BLUE}{'='*80}{ANSI_RESET}")
    renamed_str = f"{ANSI_GREEN}{success_count}{ANSI_RESET} renamed"
    errors_str = f"{ANSI_RED}{error_count}{ANSI_RESET} errors"
    print(f"Summary: {renamed_str}, {errors_str}")
    print(f"{ANSI_BLUE}{'='*80}{ANSI_RESET}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(f"Usage: python {ANSI_CYAN}rename_timestamp_files.py{ANSI_RESET} <directory_path>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        err_msg = f"Directory {ANSI_YELLOW}'{root_dir}'{ANSI_RESET} does not exist"
        print(f"{ANSI_RED}Error:{ANSI_RESET} {err_msg}")
        sys.exit(1)

    if not root_dir.is_dir():
        err_msg = f"{ANSI_YELLOW}'{root_dir}'{ANSI_RESET} is not a directory"
        print(f"{ANSI_RED}Error:{ANSI_RESET} {err_msg}")
        sys.exit(1)

    print(f"Searching in: {ANSI_CYAN}{root_dir.resolve()}{ANSI_RESET}")
    matches = find_matching_files(root_dir)

    if not matches:
        print("\nNo files matching the timestamp pattern were found.")
        sys.exit(0)

    display_dry_run(matches)

    prompt = f"\nProceed with renaming? [{ANSI_GREEN}yes{ANSI_RESET}/{ANSI_RED}no{ANSI_RESET}]: "
    response = input(prompt).strip().lower()

    if response in ('yes', 'y'):
        rename_files(matches)
    else:
        print(f"\nRenaming {ANSI_YELLOW}cancelled{ANSI_RESET}.")


if __name__ == "__main__":
    main()
