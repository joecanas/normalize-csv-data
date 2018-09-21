
# TODO: Additional development tasks

## Application Testing

* Write tests (e.g., unittest, pytest):
    - Normalization methods
    - Encoding (UTF-8, Unicode)

* Additional testing:
    - Read and write large data files (e.g., 1MB, 10MB, 100MB, 1GB)
    - Process files with 500K+ rows
    - Process long rows (e.g., > 2Kb in Address, TotalDuration, Notes)
    - Process (or reject?) very long rows (e.g., 32K/64K)
    - Pipe stdout data to other applications


## New/modified functionality (pending analysis of business requirements):

* Add (and test) stdin behavior from usage options 3-5 (see README "Usage")
* Verify business requirement for double-quoting all fields in CSV output
* Verify requirement for floating point accuracy, e.g., 3 decimal places?

* Data validations:
    - Check length, type, characters, format
    - Validate getDurationSeconds 'HH:MM:SS.MS' formatted input with regex:
      ^(([0-1][0-9])|([2][0-3])):([0-5][0-9])(:[0-5][0-9](?:[.]\d{1,3})?)?$
    - Support timestamps that already contain timezone information
    - Timestamp input (mm/dd/yy) has two-digit year; should values always be
      treated as 21st century? What about historical dates (e.g., 05/15/98)?
    - Support ZIP+4 codes
    - Support international postal codes
    - Reject empty and zero-only ZIP code values (00000 is not a valid ZIP code)
    - Reject alphanumeric ZIP codes vs. extracting and normalizing digits

* Tune behavior when a Unicode replacement character is found (currently displays error and skips a row if character found anywhere in row)
    - Skip rows only when, e.g., 'timestamp' or 'duration' would cause validation errors
    - Display stderr after stdout screen output vs. inline (current behavior)

* Add logging functionality:
    - Capture successfully processed files/rows, plus all errors
    - Write daily files, e.g., logs/normalize_2018-09-03.log
    - Meet business auditing/compliance/data storage requirements
    - Log non-standard normalizations (e.g., ZIP code alpha character removal)

* Add workflow/notification functionality (leveraging logging)

* Improve CSV input file handling:
    - Check for complete/expected header row
    - Check for at least one row of data
    - Skip blank lines
    - Skip incomplete rows (raise exception and/or log event)
    - Check for duplicate entries (based on one or more fields)?

* Batch process input files using dedicated directories:
    - Run normalizer script via cron/scheduler (or as a daemon)
    - Monitor data/in/ for input files to process
    - Write output files to data/out/[inputfilename]_YYYY-MM-DD.csv
    - Move input files to data/complete/ when done
    - Implement business rules for skipped data, e.g., skip entire file (vs. one row) and move to data/hold/
    - Implement records management process and growth plan for storing data files (e.g., capacity planning, backup, disaster recovery)

* Support additional schema and data types:
    - Create specification files, one per schema
    - Implement file naming convention, e.g., specs/unique_identifier.csv, to match data input and output files
      (data/in/unique_identifier_drop_date.csv | data/out/unique_identifier_normalized_drop_date.csv)

* Write normalized data to a database [numerous sub-tasks]
