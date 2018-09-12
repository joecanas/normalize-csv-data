import sys
import csv
import re
from datetime import datetime
import pytz


def reformatTimestamp(timestamp: str) -> str:
    # * The Timestamp column should be formatted in ISO-8601 format.
    # * The Timestamp column should be assumed to be in US/Pacific time;
    #   please convert it to US/Eastern.
    # You can assume [...] that any times that are missing timezone
    # information are in US/Pacific.
    # You can assume that the sample data we provide will contain all date
    # and time format variants you will need to handle.
    #
    # TODO (pending business requirements):
    # - Handle timestamps that contain timezone information
    timestamp = datetime.strptime(timestamp, "%m/%d/%y %I:%M:%S %p")

    pt = pytz.timezone('US/Pacific')  # Alias for ('America/Los_Angeles')
    et = pytz.timezone('US/Eastern')  # Alias for ('America/New_York')

    pt_localized = pt.normalize(pt.localize(timestamp))
    et_localized = et.normalize(pt_localized.astimezone(et))

    return et_localized.isoformat()


def rightsizeZipcode(zipcode: str) -> str:
    # * All ZIP codes should be formatted as 5 digits. If there are less
    #   than 5 digits, assume 0 as the prefix.
    #
    # TODO (pending business requirements):
    # - Support ZIP+4
    # - Reject empty and zero-only values (00000 is not a valid ZIP code)
    # - Reject alphanumeric input vs. extracting and normalizing digits
    # - Handle (or reject) non-ZIP/international postal codes
    # - If logging is implemented, report normalizations (e.g., truncations)

    # Remove all non-digit characters
    zipcode = ''.join(re.findall(r'\d+', zipcode))

    if len(zipcode) > 5:
        zipcode = zipcode[:5]

    elif len(zipcode) < 5:
        zipcode = zipcode.zfill(5)

    return zipcode


def getDurationSeconds(duration: str) -> str:
    # duration: HH:MM:SS.MS
    # @return str representing float duration in seconds
    #
    # TODO (pending business requirements):
    # - Validate HH:MM:SS.MS formatted input with regex:
    #   ^(([0-1][0-9])|([2][0-3])):([0-5][0-9])(:[0-5][0-9](?:[.]\d{1,3})?)?$
    # - Skip row or return zero if data is invalid? (business decision)
    # - If logging is implemented, log exceptions
    h, m, s = duration.split(':')
    return str(int(h) * 3600 + int(m) * 60 + float(s))


def findUnicodeReplChar(row: dict) -> list:
    # If a unicode replacement makes data invalid (for example, because it
    # turns a date field into something unparseable), print a warning to `stderr`
    # and drop the row from your output.
    unicode_repl_char = "�"
    keys_affected = []

    for key, value in row.items():
        if unicode_repl_char in value:
            keys_affected.append(key)

    return keys_affected


def main():
    # If a CSV input filename was not provided at the command line, exit with error
    if len(sys.argv) < 2:
        raise ValueError("No CSV input file provided")

    # Get the CSV input filename
    infile = sys.argv[1]

    # TODO: Improve CSV input file handling:
    # - Check for complete/expected header row
    # - Check for at least one row of data
    # - Skip blank lines
    # - Skip incomplete rows (raise exception and/or log event)
    # - Check for duplicate entries (based on one or more fields)?

    # Open the CSV input file
    with open(infile, 'r', newline='', encoding='utf-8', errors='replace') as csv_file:

        # Python 3.6+ uses OrderedDict for DictReader/DictWriter
        reader = csv.DictReader(csv_file, skipinitialspace=True)

        # TODO: Verify business requirement for double-quoting all fields in CSV output,
        # rather than quoting only fields containing commas.
        # The instructions state:
        #   "Please note there are commas in the Address field; your CSV parsing will need
        #    to take that into account. Commas will only be present inside a quoted string."
        # Commas appear in Address and Notes fields in the sample.csv input file provided.
        writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for index, row in enumerate(reader):

            # Check for Unicode replacement character, and if found, display error and skip row
            # TODO:
            # - Skip rows only when, e.g., 'timestamp' or 'duration' would cause validation errors
            # - Display stderr after stdout screen output vs. inline
            unicode_repl_char_found = findUnicodeReplChar(row)
            if len(unicode_repl_char_found) > 0:
                error_message = "Data row " + str(index + 1) \
                    + " skipped: unicode replacement character found in " \
                    + ", ".join(str(fieldname) for fieldname in unicode_repl_char_found) \

                print("Error: " + error_message, file=sys.stderr)
                continue

            # Normalize interdependent duration fields prior to insertion in output row
            row['FooDuration'] = getDurationSeconds(row['FooDuration'])
            row['BarDuration'] = getDurationSeconds(row['BarDuration'])
            row['TotalDuration'] = str(float(row['FooDuration']) + float(row['BarDuration']))

            # Under Python 3.6+, the built-in dict tracks insertion order. As of Python 3.7,
            # this is no longer an implementation detail and instead becomes a language feature.
            # From a python-dev message by GvR:
            # https://mail.python.org/pipermail/python-dev/2017-December/151283.html
            output = {
                'Timestamp': reformatTimestamp(row['Timestamp']),
                'Address': row['Address'],
                'ZIP': rightsizeZipcode(row['ZIP']),
                'FullName': row['FullName'].upper(),
                'FooDuration': row['FooDuration'],
                'BarDuration': row['BarDuration'],
                'TotalDuration': row['TotalDuration'],
                'Notes': row['Notes']
            }

            # Send normalized row to stdout
            writer.writerow(output)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print("Error: " + str(e), file=sys.stderr)


'''
TODO / ADDITIONAL DEVELOPMENT
-----------------------------

APPLICATION TESTING:

- Write tests (e.g., unittest, pytest):
  - Normalization methods
  - Encoding (UTF-8, Unicode)

- Additional testing:
  - Read and write large data files (e.g., 1MB, 10MB, 100MB, 1GB)
  - Process files with 500K+ rows
  - Process long rows (e.g., > 2Kb in Address, TotalDuration, Notes)
  - Process (or reject?) very long rows (e.g., 32K/64K)
  - Pipe stdout data to other applications


NEW/MODIFIED FUNCTIONALITY (pending business requirements):

- Add (and test) stdin behavior from usage options 3-5
- Verify business requirement for double-quoting all fields in CSV output
- Verify requirement for floating point accuracy, e.g., 3 decimal places?
- Add data validations (length, type, characters)
- Support timestamps that already contain timezone information
- Timestamp input (mm/dd/yy) has two-digit year; should values always be
  treated as 21st century? What about historical dates (e.g., 05/15/98)?
- Support ZIP+4 codes
- Support international postal codes
- Add workflow/notification functionality (leveraging logging)

- Add logging functionality:
  - Capture successfully processed files/rows, plus all errors
  - Write daily files, e.g., logs/normalize_2018-09-03.log
  - Meet business auditing/compliance/data storage requirements

- Improve CSV input file handling:
  - Check for complete/expected header row
  - Check for at least one row of data
  - Skip blank lines
  - Skip incomplete rows (raise exception and/or log event)
  - Check for duplicate entries (based on one or more fields)?

- Batch process input files using dedicated directories:
  - Run normalizer script via cron/scheduler (or as a daemon)
  - Monitor data/in/ for input files to process
  - Write output files to data/out/[inputfilename]_YYYY-MM-DD.csv
  - Move input files to data/complete/ when done
  - Implement business rules for skipped data,
    e.g., skip entire file (vs. one row) and move to data/hold/
  - Implement records management process and growth plan for storing
    data files (e.g., capacity planning, backup, disaster recovery)

- Support additional schema and data types:
  - Create specification files, one per schema
  - Implement file naming convention, e.g., specs/unique_identifier.csv,
    to match data input files (data/in/unique_identifier_drop_date.csv)
    and data output files (data/out/unique_identifier_normalized_drop_date.csv)

- Write normalized data to a database (numerous sub-tasks!)

'''
