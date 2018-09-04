
# Setup
## Requirements
* macOS 10.13 (should work on 10.10+). Will also work on Ubuntu 16.04.
* Python 3.6+
* The pytz package (for timezone functionality):

Install the package using pip at the command line:
```
pip3 install pytz
```

...or install using homebrew:
```
brew install pytz
```

If you have an older version of Python and/or need to install or update a package manager, these links may prove helpful: 
* [Python3 + pip](https://itsevans.com/install-pip-osx/)
* [homebrew](https://brew.sh/)
* [How to install pytz module on mac, Python 3.6](https://teamtreehouse.com/community/how-to-install-pytz-module-on-mac-python-36)

## Install the application script
* This is a single-script application. You can [download the git repository](https://github.com/joecanas/normalize_csv_data/archive/master.zip), but you only need the file 'normalize_csv_data.py'.
* Place the file 'normalize_csv_data.py' in the directory you'd like to use to run the application.

# Usage
The script reads data from stdin (an input file specified at the command line, or the piped or redirected data from another application. The script normalizes the data per schema-specific transformation rules, and returns the normalized data via stdout. The output can be rendered in a terminal (default), redirected to a file, or piped/redirected to another application.

1. Process a CSV file and get the normalized data returned via stdout:
Include the CSV input file's name at the command prompt (the example below assumes the file 'sample.csv' is in the same directory as the script):

```
python3 normalize_csv_data.py sample.csv
```

2. Write the normalized data to a file (the example redirects the script's stdout data to the file 'output_file.csv' in the same directory as the script):

```
python3 normalize_csv_data.py sample.csv > output_file.csv
```

3. Redirect CSV file input from another application via stdin to the script:

```
/path/to/another_program > python3 normalize_csv_data.py sample.csv
```

4. Pipe the normalized data to another application:

```
python3 normalize_csv_data.py sample.csv | /path/to/another_program
```

5. Redirect the normalized data to another application:

```
python3 normalize_csv_data.py sample.csv > /path/to/data_program

/path/to/another_program < python3 normalize_csv_data.py sample.csv
```
