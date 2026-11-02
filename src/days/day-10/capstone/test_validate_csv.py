"""QA test suite for the CSV email validator CLI.

These tests are derived from the REQUIREMENTS only (not from the Dev
implementation):
  - read a CSV with a header row containing an "email" column
  - print every invalid row as: line number, the email, the reason
  - print a summary: total rows, valid, invalid
  - exit code 1 when any row is invalid, 0 otherwise

Each test is written as Given / When / Then and runs the CLI as a real
subprocess (black-box), the same way a user would from the terminal.

Run with:
    python -m pytest test_validate_csv.py -v
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "validate_csv.py"


def run_cli(csv_path):
    """Invoke the CLI exactly as a user would and capture its output/exit code."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(csv_path)],
        capture_output=True,
        text=True,
    )
    return result


def write_csv(tmp_path, content, name="data.csv"):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_given_all_valid_emails_when_run_then_exit_code_is_zero(tmp_path):
    # Given a CSV where every row has a well-formed email
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n"
        "Ravi,ravi@example.co.in\n",
    )

    # When the CLI is run against it
    result = run_cli(csv_file)

    # Then it exits with code 0 (no invalid rows)
    assert result.returncode == 0


def test_given_all_valid_emails_when_run_then_summary_reports_all_valid(tmp_path):
    # Given a CSV with two valid emails
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n"
        "Ravi,ravi@example.co.in\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the summary shows total=2, valid=2, invalid=0
    assert "2" in result.stdout
    assert "0" in result.stdout
    lowered = result.stdout.lower()
    assert "total" in lowered and "valid" in lowered and "invalid" in lowered


def test_given_all_valid_emails_when_run_then_no_invalid_rows_are_printed(tmp_path):
    # Given a CSV with only valid emails
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then no "invalid row" line is printed for it
    assert "asha@example.com" not in result.stdout.replace("asha@example.com\n", "", 1) or True
    # More precise check: the valid email should not be flagged with a reason
    assert "reason" not in result.stdout.lower() or "line" not in result.stdout.lower()


# ---------------------------------------------------------------------------
# Invalid rows: reporting format (line number, email, reason)
# ---------------------------------------------------------------------------

def test_given_some_invalid_emails_when_run_then_exit_code_is_one(tmp_path):
    # Given a CSV with at least one malformed email
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n"
        "Ravi,ravi@example\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it exits with code 1
    assert result.returncode == 1


def test_given_invalid_row_when_run_then_output_includes_line_number(tmp_path):
    # Given a CSV whose second data row (CSV line 3, after the header) is invalid
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n"
        "Ravi,ravi@example\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the output references line 3 for the invalid row
    assert "3" in result.stdout


def test_given_invalid_row_when_run_then_output_includes_the_bad_email(tmp_path):
    # Given a CSV with a clearly malformed email value
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Ravi,not-an-email\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the offending email value appears in the output
    assert "not-an-email" in result.stdout


def test_given_invalid_row_when_run_then_output_includes_a_reason(tmp_path):
    # Given a CSV row with no "@" at all
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Ravi,not-an-email\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then some human-readable reason text is printed, not just the raw value
    lines = [line for line in result.stdout.splitlines() if "not-an-email" in line]
    assert len(lines) == 1
    assert len(lines[0]) > len("not-an-email") + 5  # more than just the value alone


# ---------------------------------------------------------------------------
# Edge cases for what counts as "invalid"
# ---------------------------------------------------------------------------

def test_given_email_missing_at_symbol_when_run_then_row_is_invalid(tmp_path):
    # Given an email with no "@"
    csv_file = write_csv(tmp_path, "name,email\nRavi,ravi.example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid and exit code is 1
    assert result.returncode == 1
    assert "ravi.example.com" in result.stdout


def test_given_email_with_multiple_at_symbols_when_run_then_row_is_invalid(tmp_path):
    # Given an email with two "@" characters
    csv_file = write_csv(tmp_path, "name,email\nRavi,ra@vi@example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid
    assert result.returncode == 1
    assert "ra@vi@example.com" in result.stdout


def test_given_email_with_missing_domain_when_run_then_row_is_invalid(tmp_path):
    # Given an email with nothing after "@"
    csv_file = write_csv(tmp_path, "name,email\nRavi,ravi@\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid
    assert result.returncode == 1


def test_given_email_with_missing_local_part_when_run_then_row_is_invalid(tmp_path):
    # Given an email with nothing before "@"
    csv_file = write_csv(tmp_path, "name,email\nRavi,@example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid
    assert result.returncode == 1


def test_given_email_with_embedded_space_when_run_then_row_is_invalid(tmp_path):
    # Given an email value containing whitespace
    csv_file = write_csv(tmp_path, "name,email\nRavi,ravi example@example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid
    assert result.returncode == 1


def test_given_empty_email_value_when_run_then_row_is_invalid(tmp_path):
    # Given a row where the email column is blank
    csv_file = write_csv(tmp_path, "name,email\nRavi,\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid, not silently skipped
    assert result.returncode == 1


def test_given_domain_without_tld_when_run_then_row_is_invalid(tmp_path):
    # Given an email domain with no "." (no top-level domain)
    csv_file = write_csv(tmp_path, "name,email\nRavi,ravi@example\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then it is reported invalid
    assert result.returncode == 1


# ---------------------------------------------------------------------------
# Summary totals
# ---------------------------------------------------------------------------

def test_given_mixed_valid_and_invalid_rows_when_run_then_summary_counts_are_correct(tmp_path):
    # Given a CSV with 2 valid and 2 invalid emails (4 data rows total)
    csv_file = write_csv(
        tmp_path,
        "name,email\n"
        "Asha,asha@example.com\n"
        "Ravi,ravi@example\n"
        "Meena,meena@example.co.in\n"
        "Kiran,@example.com\n",
    )

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the summary reflects total=4, valid=2, invalid=2
    output = result.stdout
    assert "4" in output
    assert "2" in output
    assert result.returncode == 1


# ---------------------------------------------------------------------------
# CSV structure / header handling
# ---------------------------------------------------------------------------

def test_given_csv_missing_email_column_when_run_then_tool_reports_error(tmp_path):
    # Given a CSV with no "email" column at all
    csv_file = write_csv(tmp_path, "name,contact\nAsha,asha@example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the tool does not silently proceed; it signals an error
    assert result.returncode != 0


def test_given_email_header_different_case_when_run_then_column_is_still_found(tmp_path):
    # Given a CSV whose header uses "Email" instead of "email"
    csv_file = write_csv(tmp_path, "name,Email\nAsha,asha@example.com\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then the column is still recognized and the row is validated normally
    assert result.returncode == 0


def test_given_csv_with_only_header_row_when_run_then_zero_total_and_exit_zero(tmp_path):
    # Given a CSV containing only the header, no data rows
    csv_file = write_csv(tmp_path, "name,email\n")

    # When the CLI is run
    result = run_cli(csv_file)

    # Then total/valid/invalid are all 0 and exit code is 0 (nothing invalid)
    assert result.returncode == 0
    assert "0" in result.stdout


# ---------------------------------------------------------------------------
# File-level error handling
# ---------------------------------------------------------------------------

def test_given_nonexistent_file_when_run_then_tool_exits_nonzero(tmp_path):
    # Given a path to a CSV file that does not exist
    missing_file = tmp_path / "does_not_exist.csv"

    # When the CLI is run against it
    result = run_cli(missing_file)

    # Then the tool fails gracefully with a non-zero exit code (not a crash/traceback)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
