"""
Email Extractor CLI (Typer)

This script provides a command-line interface (CLI) for extracting email addresses from various sources, including an ICS calendar file, a text file with name-email pairs, and a text file with newline-separated email addresses. It then combines all the unique email addresses and writes them to a file.

Usage:
    python email_extractor_cli_typer.py --ics-file invite.ics --start-date 2023-08-01 --end-date 2024-01-01 --name-email-file email_list_from_last_year_minis.txt --newline-email-file emails_from_usession.txt --output-file 2024_sarah_dowell_photography_mini_session_past_clients.txt

Options:
  --ics-file TEXT                Path to the .ics calendar file  [required]
  --start-date TEXT              Start date for the date range filter (YYYY-MM-DD)
  --end-date TEXT                End date for the date range filter (YYYY-MM-DD)
  --name-email-file TEXT...      Path(s) to the text file(s) with name-email pairs
  --newline-email-file TEXT      Path to the text file with newline-separated email addresses
  --output-file TEXT             Path to the output file for the combined email list  [required]
  --help                         Show this message and exit.

The script will extract email addresses from the provided sources, combine them, and write the unique email addresses to the specified output file.

Example Usage:

```bash
python email_extractor_cli.py --ics-file invite.ics --start-date 2023-08-01 --end-date 2024-01-01 --name-email-file email_list_from_last_year_minis.txt --newline-email-file emails_from_usession.txt --output-file 2024_sarah_dowell_photography_mini_session_past_clients.txt
```
"""

import typer
from datetime import datetime
from typing import List, Optional
from email_extractor import (
    ics_to_dataframe,
    extract_email_addresses,
    clean_and_explode_emails,
    extract_emails_from_text,
    extract_emails_from_newline_separated_text,
)

app = typer.Typer()


@app.command()
def extract_emails(
    ics_file: str = typer.Option(
        ..., "--ics-file", help="Path to the .ics calendar file"
    ),
    start_date: Optional[str] = typer.Option(
        None, "--start-date", help="Start date for the date range filter (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = typer.Option(
        None, "--end-date", help="End date for the date range filter (YYYY-MM-DD)"
    ),
    name_email_file: List[str] = typer.Option(
        None,
        "--name-email-file",
        help="Path(s) to the text file(s) with name-email pairs",
    ),
    newline_email_file: Optional[str] = typer.Option(
        None,
        "--newline-email-file",
        help="Path to the text file with newline-separated email addresses",
    ),
    output_file: str = typer.Option(
        ..., "--output-file", help="Path to the output file for the combined email list"
    ),
):
    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    df = ics_to_dataframe(ics_file, start_date=start_date, end_date=end_date)
    df = extract_email_addresses(df)
    df = clean_and_explode_emails(df)
    emails_from_calendar = list(df.Emails.unique())

    emails_from_last_years_minis: List[str] = []
    if name_email_file:
        emails_from_last_years_minis = extract_emails_from_text(name_email_file)

    emails_from_u_session: List[str] = []
    if newline_email_file:
        emails_from_u_session = extract_emails_from_newline_separated_text(
            newline_email_file
        )

    emails = set(
        emails_from_u_session + emails_from_calendar + emails_from_last_years_minis
    )

    with open(output_file, "w") as file:
        file.write("\n".join(emails))

    typer.echo(f"Email list saved to: {output_file}")


if __name__ == "__main__":
    app()