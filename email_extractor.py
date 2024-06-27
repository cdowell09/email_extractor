"""
Email Extractor Script

This script extracts email addresses from various sources, including an ICS calendar file, a text file with name-email pairs, and a text file with newline-separated email addresses. It then combines all the unique email addresses and writes them to a file.

The script provides the following main functions:

1. `ics_to_dataframe`: Converts an .ics calendar file to a Pandas DataFrame, optionally filtering by a date range.
2. `extract_email_addresses`: Extracts email addresses from the 'Attendees' column of a DataFrame.
3. `clean_and_explode_emails`: Cleans and explodes the 'Emails' column of a DataFrame, creating one email per row.
4. `extract_emails_from_text`: Extracts email addresses from one or more text files containing name-email pairs.
5. `extract_emails_from_newline_separated_text`: Extracts email addresses from a text file where the email addresses are separated by newlines.

The script also includes example usage at the end, demonstrating how to use the functions to extract and combine email addresses from various sources, and write the resulting set of unique email addresses to a file.

Usage:
1. Ensure the required dependencies (pandas, icalendar, pytz, re) are installed.
2. Provide the necessary file paths for the ICS calendar file, the name-email pair text file, and the newline-separated email text file.
3. Run the script to generate the combined email list and write it to the output file.

Note: This script is designed to be reusable and adaptable to different email data sources and requirements. Feel free to modify or extend the functionality as needed.
"""

import pandas as pd
from icalendar import Calendar, vCalAddress
from datetime import datetime
from typing import Optional, List
import pytz
import re


def ics_to_dataframe(
    ics_file: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    Convert an .ics calendar file to a Pandas DataFrame.

    Parameters:
        ics_file (str): The path to the .ics file.
        start_date (datetime.datetime, optional): The start date for the date range filter. If not provided, no date filtering will be applied.
        end_date (datetime.datetime, optional): The end date for the date range filter. If not provided, no date filtering will be applied.

    Returns:
        pandas.DataFrame: A DataFrame containing the calendar events.
    """
    with open(ics_file, "rb") as file:
        gcal = Calendar.from_ical(file.read())

    events = []
    for component in gcal.walk("VEVENT"):
        attendees = []
        for attendee in component.get("attendee", []):
            if isinstance(attendee, vCalAddress):
                attendees.append(attendee.params["CN"])
            else:
                attendees.append(attendee)

        start_dt = component.get("dtstart").dt
        end_dt = component.get("dtend").dt if component.get("dtend") else None

        # Convert timezone-aware datetime objects to UTC
        if isinstance(start_dt, datetime):
            start_dt = start_dt.astimezone(pytz.utc)
        if isinstance(end_dt, datetime):
            end_dt = end_dt.astimezone(pytz.utc)

        event = {
            "Summary": component.get("summary"),
            "Start": start_dt,
            "End": end_dt,
            "Location": component.get("location"),
            "Description": component.get("description"),
            "Attendees": ", ".join(attendees),
        }
        events.append(event)

    df = pd.DataFrame(events)
    df["Start"] = pd.to_datetime(df["Start"], utc=True)
    df["End"] = pd.to_datetime(df["End"], utc=True)

    # Filter events by date range if start_date and end_date are provided
    if start_date and end_date:
        df = df[
            (df["Start"].dt.tz_localize(None) >= start_date)
            & (df["Start"].dt.tz_localize(None) < end_date)
        ]

    return df


def extract_email_addresses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract email addresses from the 'Attendees' column of the input DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the 'Attendees' column.

    Returns:
        pandas.DataFrame: The input DataFrame with a new 'Emails' column containing the extracted email addresses.
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    df["Emails"] = df["Attendees"].apply(
        lambda attendees: ", ".join(re.findall(email_pattern, attendees))
    )

    return df


def clean_and_explode_emails(df: pd.DataFrame) -> pd.DataFrame:
    """
    1. Drops any observations in the DataFrame where the 'Emails' column is empty.
    2. Explodes the 'Emails' column to have one email per row.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the 'Emails' column.

    Returns:
        pandas.DataFrame: The cleaned and exploded DataFrame.
    """
    # Drop rows with empty emails
    df = df[df["Emails"].astype(bool)]

    # Split the 'Emails' column by comma and explode
    df = df.assign(Emails=df["Emails"].str.split(",")).explode("Emails")

    # Strip whitespace from email addresses
    df["Emails"] = df["Emails"].str.strip()

    return df


def extract_emails_from_text(file_paths: List[str]) -> List[str]:
    """
    Extract email addresses from one or more text files containing name-email pairs.

    Parameters:
        file_paths (List[str]): A list of file paths to the text files.

    Returns:
        List[str]: A list of extracted email addresses.
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = []

    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
            emails.extend(re.findall(email_pattern, content))

    return emails


def extract_emails_from_newline_separated_text(file_path: str) -> List[str]:
    """
    Extract email addresses from a text file where the email addresses are separated by newlines.

    Parameters:
        file_path (str): The path to the text file.

    Returns:
        List[str]: A list of extracted email addresses.
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = []

    with open(file_path, "r") as file:
        for line in file:
            email = line.strip()
            if re.match(email_pattern, email):
                emails.append(email)

    return emails


# # Example usage
# start_date = datetime(2023, 8, 1)
# end_date = datetime(2024, 1, 1)
# df = ics_to_dataframe("invite.ics", start_date=start_date, end_date=end_date)
# df = extract_email_addresses(df)
# df = clean_and_explode_emails(df)
# emails_from_calendar = list(df.Emails.unique())

# emails_from_last_years_minis = extract_emails_from_text(
#     ["email_list_from_last_year_minis.txt"]
# )
# emails_from_u_session = extract_emails_from_newline_separated_text(
#     "emails_from_usession.txt"
# )

# emails = set(
#     emails_from_u_session + emails_from_calendar + emails_from_last_years_minis
# )

# # Write emails to file
# with open("2024_sarah_dowell_photography_mini_session_past_clients.txt", "w") as file:
#     file.write("\n".join(emails))
