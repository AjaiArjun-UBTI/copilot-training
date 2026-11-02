# Capstone PR: CSV Email Validator CLI

Pair: Ajai (Dev) + Ajai (QA)
Branch: capstone/AjaiArjun (does not need to merge to main)

## What it does
A Python CLI tool, [validate_csv.py](./validate_csv.py), that reads a CSV file, validates the
value in its "email" column for every row, and reports which rows are invalid and why, along
with a summary of total/valid/invalid counts. Built with stdlib only (`csv`, `re`, `sys`) —
no external dependencies.

## Requirements
- [x] Read a CSV with a header row containing an "email" column (case-insensitive match)
- [x] Print every invalid row as: line number, the email, the reason
- [x] Print a summary: total rows, valid, invalid
- [x] Exit code 1 when any row is invalid, 0 otherwise

## Test evidence

**Automated tests** — [test_validate_csv.py](./test_validate_csv.py), 19 black-box test cases
written directly from the requirements above (Given-When-Then), run via subprocess against the
real CLI (not against internal functions):

```
python -m pytest test_validate_csv.py -v

============================= test session starts =============================
collected 19 items

test_validate_csv.py::test_given_all_valid_emails_when_run_then_exit_code_is_zero PASSED
test_validate_csv.py::test_given_all_valid_emails_when_run_then_summary_reports_all_valid PASSED
test_validate_csv.py::test_given_all_valid_emails_when_run_then_no_invalid_rows_are_printed PASSED
test_validate_csv.py::test_given_some_invalid_emails_when_run_then_exit_code_is_one PASSED
test_validate_csv.py::test_given_invalid_row_when_run_then_output_includes_line_number PASSED
test_validate_csv.py::test_given_invalid_row_when_run_then_output_includes_the_bad_email PASSED
test_validate_csv.py::test_given_invalid_row_when_run_then_output_includes_a_reason PASSED
test_validate_csv.py::test_given_email_missing_at_symbol_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_email_with_multiple_at_symbols_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_email_with_missing_domain_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_email_with_missing_local_part_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_email_with_embedded_space_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_empty_email_value_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_domain_without_tld_when_run_then_row_is_invalid PASSED
test_validate_csv.py::test_given_mixed_valid_and_invalid_rows_when_run_then_summary_counts_are_correct PASSED
test_validate_csv.py::test_given_csv_missing_email_column_when_run_then_tool_reports_error PASSED
test_validate_csv.py::test_given_email_header_different_case_when_run_then_column_is_still_found PASSED
test_validate_csv.py::test_given_csv_with_only_header_row_when_run_then_zero_total_and_exit_zero PASSED
test_validate_csv.py::test_given_nonexistent_file_when_run_then_tool_exits_nonzero PASSED

============================= 19 passed in 5.05s ==============================
```

**Manual run** against [sample.csv](./sample.csv) (edge case: blank email, missing `@`, missing
domain TLD, embedded whitespace, all mixed with valid rows):

```
python validate_csv.py sample.csv

Line 3: 'ravi@example' - domain missing a top-level domain (e.g. .com)
Line 5: '@example.com' - missing local part before @
Line 6: 'divya example@example.com' - contains whitespace
Line 7: '' - missing email

Summary:
  Total rows:   7
  Valid rows:   3
  Invalid rows: 4
EXIT CODE: 1
```
Exit code 1 confirmed via `$LASTEXITCODE`, matching the requirement that any invalid row
triggers a non-zero exit.

Edge cases specifically covered: missing `email` header column, header name with different
case (`Email`), CSV with only a header row and no data, blank email value, and a
nonexistent file path (handled gracefully with a non-zero exit, no stack trace).

## Copilot usage notes (required)
| Step | What Copilot was used for | What we kept / rewrote / rejected, and why |
|---|---|---|
| Scaffold | Generated the initial CLI skeleton and confirmed the requirement list (CSV read, invalid-row reporting, summary, exit codes) from a plain-language prompt. | Kept the skeleton as the starting structure; added real logic ourselves since the scaffold had no implementation yet. |
| Implementation | Generated `validate_email()` validation rules (missing/duplicate `@`, missing local/domain part, whitespace, missing TLD) and the `csv.DictReader`-based row loop with case-insensitive header matching. | Kept most of it; rewrote some validation messages to be clearer and confirmed the regex matched our own manual test emails before accepting it. |
| Tests | Generated the 19 Given-When-Then pytest cases directly from the requirements (not from the implementation), covering happy path, reporting format, invalid-email edge cases, header/structure edge cases, and file errors. | Kept all 19 after running them against the implementation and confirming they failed appropriately when logic was intentionally broken during a sanity check, then passed against the real code. |
| Review | Used Copilot to review the PR description/template wording and to double-check the branch name and governance checklist formatting. | Rewrote the vague "Test evidence" and "Copilot usage notes" sections rejected in the first draft, replacing "yes"/"everything was kept" with concrete detail. |

## Governance check
- [x] No secrets, credentials, customer PII or proprietary algorithms were pasted into any prompt
- [x] Security checklist applied (secrets, input validation, crypto, PII in logs) — input validation is the core feature; no secrets or PII handled/logged by this tool
- [x] A human reviewed every suggestion before it was kept
