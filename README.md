# Email Extractor CLI

This Python script provides a command-line interface (CLI) for extracting email addresses from various sources, including an ICS calendar file, a text file with name-email pairs, and a text file with newline-separated email addresses. It then combines all the unique email addresses and writes them to a file.

## Installation

### Cloning the Repository

1. Clone the repository and navigate to the project directory:

```
git clone https://github.com/cdowell09/email-extractor.git
cd email-extractor
```

### Using pip

1. Make sure you have Python 3.x installed on your system.
2. Install the required dependencies using pip:

```
pip install typer pandas icalendar pytz
```

### Using Poetry

1. Install Poetry, if you haven't already: https://python-poetry.org/docs/#installation
2. Navigate to the project directory (assuming you've already cloned the repository):

```
cd email-extractor
```

3. Install the project dependencies using Poetry:

```
poetry install
```

## Usage

```
python email_extractor_cli_typer.py --ics-file invite.ics --start-date 2023-08-01 --end-date 2024-01-01 --name-email-file email_list_from_last_year_minis.txt --newline-email-file emails_from_usession.txt --output-file all_unique_emails_combined.txt
```

## Options

- `--ics-file`: Path to the .ics calendar file (required)
- `--start-date`: Start date for the date range filter (YYYY-MM-DD)
- `--end-date`: End date for the date range filter (YYYY-MM-DD)
- `--name-email-file`: Path(s) to the text file(s) with name-email pairs. This file should look like this:
```
Tim Cook <timcook@gmail.com>,
Eileen Dover <eileendover@live.com>,
...
```
- `--newline-email-file`: Path to the text file with newline-separated email addresses. This file should look like this:
```
timcook@gmail.com
eileendover@live.com
```

- `--output-file`: Path to the output file for the combined email list (required)

## Dependencies

Dependencies are shown in the `pyproject.toml` file.