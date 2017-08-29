from __future__ import print_function

from datetime import date
import os
from ftplib import FTP
import re

from lookups import FIRST_FISCAL_YEAR, GARBAGE_STRINGS

current_path = os.path.dirname(os.path.abspath(__file__))
raw_data_dir = os.path.abspath(
    os.path.join(current_path, os.pardir, 'raw_data'))


def get_date_obj(d):
    """Return a date object from a payroll record date string."""

    try:
        year = d[:4]
        month = d[4:6]
        day = d[6:8]
        return date(int(year), int(month), int(day))
    except:
        return date(1900, 1, 1)


def in_fiscal_year(date_obj):
    """Does this date fall within the fiscal year?"""

    fiscal_start = date(FIRST_FISCAL_YEAR, 7, 1)
    fiscal_end = date(FIRST_FISCAL_YEAR+1, 6, 30)

    return fiscal_start <= date_obj <= fiscal_end


def download_payroll_data():
    """Download payroll and lookup files."""

    # connect to the FTP server
    ftp = FTP(os.environ['OK_STATE_FTP_HOST'],
              os.environ['OK_STATE_FTP_USERNAME'],
              os.environ['OK_STATE_FTP_PASSWORD'])

    # get a list of the files
    files = ftp.nlst()

    # use regex to target payroll files
    target_years_regex = ''.join([
        '(',
        str(FIRST_FISCAL_YEAR)[2:],
        '|',
        str(FIRST_FISCAL_YEAR+1)[2:],
        ')'
    ])

    pattern = re.compile('CALP' + target_years_regex + '\d{2}.DAT')
    payroll_files = [x.group(0) for q in files for x
                     in [pattern.search(q)] if x]

    # loop over that list, downloading each file
    # ... checking first to see if it already exists
    for file in payroll_files:
        if file not in os.listdir(raw_data_dir):
            print('            ' + file)
            ftp.retrbinary('RETR ' + file,
                           open(os.path.join(raw_data_dir, file), 'wb').write)

    # download the lookup files
    ftp.retrbinary('RETR AGCYINFO.DAT',
                   open(os.path.join(raw_data_dir, 'agency_list.DAT'), 'wb').write)  # NOQA
    ftp.retrbinary('RETR OBJCTCD.DAT',
                   open(os.path.join(raw_data_dir, 'paycode_list.DAT'), 'wb').write)  # NOQA

    # disconnect
    ftp.quit()


def get_unique_ids(data_file, extra_var, slice_num):
    """Return a unique list of agency or payroll codes."""

    # Start with a list of codes
    # that have appeared in previous data sets but not
    # in the master file
    codes = extra_var

    # Then loop over the master file
    with open(data_file, 'r') as d:
        data = d.readlines()
        for row in data:
            code = str(row[:slice_num])
            name = row[slice_num:].strip()

            # a little name cleanup
            for item in GARBAGE_STRINGS:
                name = name.replace(*item)
            codes[code] = name

    return codes
