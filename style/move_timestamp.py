"""Recursively rename files by moving timestamp from filename to description."""

import re
import sys
from pathlib import Path
from typing import List, Tuple

from utils.style import ansi


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
    print("\n" + f"{ansi.blue}{'='*80}{ansi.reset}")
    print(f"{ansi.yellow}DRY RUN{ansi.reset} - Files that would be renamed:")
    print(f"{ansi.blue}{'='*80}{ansi.reset}\n")

    for file_path, new_filename in matches:
        print(f"FROM: {ansi.red}{file_path.name}{ansi.reset}")
        print(f"  TO: {ansi.green}{new_filename}{ansi.reset}")
        print()

    print(f"\nTotal files to rename: {ansi.green}{len(matches)}{ansi.reset}")


def rename_files(matches: List[Tuple[Path, str]]) -> None:
    """Actually rename the files."""
    print("\n" + f"{ansi.blue}{'='*80}{ansi.reset}")
    print(f"{ansi.magenta}Renaming files...{ansi.reset}")
    print(f"{ansi.blue}{'='*80}{ansi.reset}\n")

    success_count = 0
    error_count = 0

    for file_path, new_filename in matches:
        try:
            new_path = file_path.parent / new_filename
            file_path.rename(new_path)
            print(f"{ansi.green}✓{ansi.reset} {ansi.cyan}{file_path.name}{ansi.reset}")
            success_count += 1
        except OSError as e:
            print(f"{ansi.red}✗{ansi.reset} Error renaming {ansi.yellow}{file_path.name}{ansi.reset}: {ansi.red}{e}{ansi.reset}")
            error_count += 1

    print("\n" + f"{ansi.blue}{'='*80}{ansi.reset}")
    print(f"Summary: {ansi.green}{success_count}{ansi.reset} renamed, {ansi.red}{error_count}{ansi.reset} errors")
    print(f"{ansi.blue}{'='*80}{ansi.reset}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(f"Usage: python {ansi.cyan}rename_timestamp_files.py{ansi.reset} <directory_path>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        print(f"{ansi.red}Error:{ansi.reset} Directory {ansi.yellow}'{root_dir}'{ansi.reset} does not exist")
        sys.exit(1)

    if not root_dir.is_dir():
        print(f"{ansi.red}Error:{ansi.reset} {ansi.yellow}'{root_dir}'{ansi.reset} is not a directory")
        sys.exit(1)

    print(f"Searching in: {ansi.cyan}{root_dir.resolve()}{ansi.reset}")
    matches = find_matching_files(root_dir)

    if not matches:
        print("\nNo files matching the timestamp pattern were found.")
        sys.exit(0)

    display_dry_run(matches)

    response = input(f"\nProceed with renaming? [{ansi.green}yes{ansi.reset}/{ansi.red}no{ansi.reset}]: ").strip().lower()

    if response in ('yes', 'y'):
        rename_files(matches)
    else:
        print(f"\nRenaming {ansi.yellow}cancelled{ansi.reset}.")


if __name__ == "__main__":
    main()
