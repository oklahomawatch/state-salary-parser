# Updating the Oklahoma Watch salaries database
This repository has the scripts you'll need to download, transform and load new data into Oklahoma Watch's state and educational salaries databases.

## Setup
Before you begin, you'll need:

* Python (2 or 3, shouldn't matter)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/) or, better, [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/)
* Login credentials for state FTP and OKW servers

### Environmental variables
You'll need these environmental variables to download the raw data.

* *`OK_STATE_FTP_HOST`*: State FTP host
* *`OK_STATE_FTP_USERNAME`*: State FTP username
* *`OK_STATE_FTP_PASSWORD`*: State FTP password

## Setup
Set your environmental variables and clone this repo. Then:
```shell
$ virtualenv ok-salaries && cd ok-salaries
$ source bin/activate
$ pip install -r requirements.txt
```

Or, if you're using `virtualenvwrapper`:
```shell
$ cd ok-salaries
$ mkvirtualenv ok-salaries
$ pip install -r requirements.txt
```

The scripts live in `./parser`:

- `lookups.py`: Lookups to determine which files to target and manage some text processing. You need to set the int variable `FIRST_FISCAL_YEAR` to the first calendar year of the fiscal year for which you need data. For instance, if you are getting data fo FY15-16, you would enter `2015`.
- `models.py`: Contains the `PayrollRecord` class we use to help organize the data.
- `parser.py`: The main script you'll call to kick things off.
- `utils.py`: The function to download the raw data + some convenience functions.

## General overview

- Download raw data from the state's FTP server. The files land in `./raw_data`.
- Clean, transform and aggregate into something our Django DB can ingest. These files land in `./parsed_data`.
- Kill and fill the data in Django.

If the parsing script runs into an agency or pay code in the data that's not in the master lists -- or the supplemental lists from `./lookups` -- it writes those files out to `./fixme`. That's when you pick up the phone and call a data specialist over in state payroll.

## Running the update script
Running `$ python parser/parser.py` calls the functions in order.

## Uploading the files
At the moment, still a manual process, sorry. Use PHPMyAdmin. The tilde-delimited files created:

- `edu-agencies-ready-to-upload.txt`
- `state-agencies-ready-to-upload.txt`
- `edu-personnel-ready-to-upload.txt`
- `state-personnel-ready-to-upload.txt`

## Known issues

- The state doesn't release unique ID numbers for its employees, so we group pay records by name and hire date, for regular state employees, or by name, agency ID and job code for higher-education workers. It's therefore possible that a higher-ed employee who changes jobs (or agencies) mid-year could show up twice in the data. It's also possible, though less likely, that multiple state employees with identical first, middle and last names, hired on the same day, could be treated as one person.

- Employees with names like NULL or NA (there are a handful) are interpreted literally by pandas as null values. This problem is solved by setting `keep_default_na=False` when creating the data frames.

- A handful of payments to "ESTATE O," which are incomplete, are excluded from the analysis.
