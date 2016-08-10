# Updating the Oklahoma Watch salaries database
Instructions for uploading new data into Oklahoma Watch's state and educational salaries database.

## Requirements
* python2.7 (fabric doesn't work with python3)
* virtualenv or virtualenvwrapper
* login credentials for state and OKW servers

## Environmental variables
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

You now have access to:
* [`fabric`](http://www.fabfile.org/)
* [`awesome-slugify`](https://pypi.python.org/pypi/awesome-slugify/1.6.5)
* [`pandas`](http://pandas.pydata.org/)

In `fabfile.py`, set the int variable `FIRST_FISCAL_YEAR` to the first calendar year of the fiscal year for which you need data. For instance, if you are getting data fo FY15-16, you would enter 2015.

## General overview
* Download raw data from the state's FTP server.
* Clean, transform and aggregate into something our Django DB can ingest.
* Kill and fill the data in Django.

## Fabric commands
* `fab download_payroll_data`: download the data and lookup files
* `fab parse_payroll_data`: translate the raw data and dump to intermediate files
* `fab aggregate_payroll_data`: run the aggregations and dump to ready-to-upload files

## Running the update script
Running `$ ./update.sh` calls all of the fabric commands in order.

## Uploading the files
Still a manual process.

## Known issues
* The state doesn't release unique ID numbers for its employees, so we group pay records by name and hire date, for regular state employees, or by name, agency ID and job code for higher-education workers. It's therefore possible that a higher-ed employee who changes jobs (or agencies) mid-year could show up twice in the data. It's also possible, though less likely, that multiple state employees with identical first, middle and last names, hired on the same day, could be treated as one person.
* Employees with names like NULL or NA (there are a handful) are interpreted literally by pandas as null values. This problem is solved by setting `keep_default_na=False` when creating the data frames.
* A handful of payments to "ESTATE O," which are incomplete, are excluded from the analysis.
