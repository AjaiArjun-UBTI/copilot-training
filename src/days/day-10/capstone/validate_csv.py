#!/usr/bin/env python3
"""Capstone option A: CSV email validator CLI.

Usage: python validate_csv.py sample.csv

Requirements:
 - read a CSV with a header row containing an "email" column
 - print every invalid row as: line number, the email, the reason
 - print a summary: total rows, valid, invalid
 - exit code 1 when any row is invalid, 0 otherwise
 - no external dependencies (stdlib only)
"""

import csv
import re
import sys

# Simple, readable email pattern: local@domain.tld
# local part: letters, digits, and . _ % + - (no whitespace, no leading/trailing dot)
# domain: at least one dot, labels of letters/digits/hyphen, final label alphabetic only
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
)


def validate_email(email):
    """Return None if the email is valid, otherwise a short reason string."""
    if email is None or email.strip() == "":
        return "missing email"

    if email != email.strip():
        return "contains leading/trailing whitespace"

    if " " in email:
        return "contains whitespace"

    if email.count("@") == 0:
        return "missing @"

    if email.count("@") > 1:
        return "contains more than one @"

    local, _, domain = email.partition("@")
    if local == "":
        return "missing local part before @"

    if domain == "":
        return "missing domain after @"

    if "." not in domain:
        return "domain missing a top-level domain (e.g. .com)"

    if not EMAIL_PATTERN.match(email):
        return "invalid email format"

    return None


def find_email_column(fieldnames):
    """Find the name of the column that represents the email, case-insensitive."""
    if not fieldnames:
        return None
    for name in fieldnames:
        if name is not None and name.strip().lower() == "email":
            return name
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_csv.py <path-to-csv>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    try:
        with open(path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            email_column = find_email_column(reader.fieldnames)
            if email_column is None:
                print('Error: CSV is missing an "email" column header.', file=sys.stderr)
                sys.exit(1)

            total = 0
            valid = 0
            invalid = 0

            for row in reader:
                total += 1
                line_number = reader.line_num
                email = row.get(email_column)

                reason = validate_email(email)
                if reason is None:
                    valid += 1
                else:
                    invalid += 1
                    print(f"Line {line_number}: '{email}' - {reason}")

    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"Error: could not read file: {error}", file=sys.stderr)
        sys.exit(1)

    print()
    print("Summary:")
    print(f"  Total rows:   {total}")
    print(f"  Valid rows:   {valid}")
    print(f"  Invalid rows: {invalid}")

    sys.exit(1 if invalid > 0 else 0)


if __name__ == "__main__":
    main()
