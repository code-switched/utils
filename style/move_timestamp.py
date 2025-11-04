"""Recursively rename files by moving timestamp from filename to description."""

import re
import sys
from pathlib import Path
from typing import List, Tuple


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
    print("\n" + "="*80)
    print("DRY RUN - Files that would be renamed:")
    print("="*80 + "\n")

    for file_path, new_filename in matches:
        print(f"FROM: {file_path}")
        print(f"  TO: {file_path.parent / new_filename}")
        print()

    print(f"\nTotal files to rename: {len(matches)}")


def rename_files(matches: List[Tuple[Path, str]]) -> None:
    """Actually rename the files."""
    print("\n" + "="*80)
    print("Renaming files...")
    print("="*80 + "\n")

    success_count = 0
    error_count = 0

    for file_path, new_filename in matches:
        try:
            new_path = file_path.parent / new_filename
            file_path.rename(new_path)
            print(f"✓ {file_path.name}")
            success_count += 1
        except Exception as e:
            print(f"✗ Error renaming {file_path.name}: {e}")
            error_count += 1

    print("\n" + "="*80)
    print(f"Summary: {success_count} renamed, {error_count} errors")
    print("="*80)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python rename_timestamp_files.py <directory_path>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        print(f"Error: Directory '{root_dir}' does not exist")
        sys.exit(1)

    if not root_dir.is_dir():
        print(f"Error: '{root_dir}' is not a directory")
        sys.exit(1)

    print(f"Searching in: {root_dir.resolve()}")
    matches = find_matching_files(root_dir)

    if not matches:
        print("\nNo files matching the timestamp pattern were found.")
        sys.exit(0)

    display_dry_run(matches)

    response = input("\nProceed with renaming? (yes/no): ").strip().lower()

    if response in ('yes', 'y'):
        rename_files(matches)
    else:
        print("\nRenaming cancelled.")


if __name__ == "__main__":
    main()
