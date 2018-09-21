import sys
import csv
import re
from datetime import datetime
import pytz


def reformatTimestamp(timestamp: str) -> str:
    timestamp = datetime.strptime(timestamp, "%m/%d/%y %I:%M:%S %p")

    pt = pytz.timezone('US/Pacific')
    et = pytz.timezone('US/Eastern')

    pt_localized = pt.normalize(pt.localize(timestamp))
    et_localized = et.normalize(pt_localized.astimezone(et))

    return et_localized.isoformat()


def rightsizeZipcode(zipcode: str) -> str:
    # Remove all non-digit characters
    zipcode = ''.join(re.findall(r'\d+', zipcode))

    if len(zipcode) > 5:
        zipcode = zipcode[:5]
    elif len(zipcode) < 5:
        zipcode = zipcode.zfill(5)

    return zipcode


def getDurationSeconds(duration: str) -> str:
    h, m, s = duration.split(':')
    return str(int(h) * 3600 + int(m) * 60 + float(s))


def findUnicodeReplChar(row: dict) -> list:
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

    with open(infile, 'r', newline='', encoding='utf-8', errors='replace') as csv_file:
        reader = csv.DictReader(csv_file, skipinitialspace=True)
        writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for index, row in enumerate(reader):
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

            writer.writerow(output)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print("Error: " + str(e), file=sys.stderr)
