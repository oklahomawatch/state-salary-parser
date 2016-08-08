from os import environ, listdir
import re
import csv
from datetime import date
from ftplib import FTP

from fabric.api import *
from fabric.operations import *
from fabric.state import output as fab_output

import pandas as pd

from slugify import slugify

from lookups import (EDU_AGENCIES, GARBAGE_STRINGS,
                     EXTRA_EDU_AGENCIES, EXTRA_PAYROLL_CODES)


# quiet output from fabric tasks
fab_output.status = False

# set this numeric variable as the first year of the
# fiscal year you're targeting - e.g., "2015" for
# FY15-16 ending June 30, 2016
FIRST_FISCAL_YEAR = 2015


class PayrollRecord(object):
    """A record of a payment to a state or higher-ed employee."""

    def __init__(self, row):
        self._raw_data = row
        self.agency_id = row[17:20].strip()
        self.last_name = row[80:110].strip()
        self.first_name = row[20:50].strip()
        self.middle_name = row[50:80].strip()
        self.job_code = row[110:117].strip()
        self.pay_code = row[150:154].strip()
        self.job_title = row[154:184].strip()
        self.hire_date = get_date_obj(row[186:].strip())
        self.payment_date = get_date_obj(row[123:131].strip())

        # divide by 100 to get actual payment amount
        # per instructions from state data folk
        self.amount = float(int(row[141:150].strip())) / 100
        
        # TODO: add assertions to validate data
        
    # method to get full name
    def full_name(self):
        name = "{} {} {}".format(
            self.first_name,
            self.middle_name,
            self.last_name
        )

        # remove multiple spaces
        return " ".join(name.split())

    # method to get first and middle names
    def first_and_middle_name(self):
        name = "{} {}".format(
            self.first_name,
            self.middle_name
        )

        # remove multiple spaces
        return " ".join(name.split())

    # check if hire date is valid
    def has_valid_hire_date(self):
        return self.hire_date != date(1900, 1, 1)

    # does this person work in higher ed?
    def is_education_employee(self):
        return str(self.agency_id) in EDU_AGENCIES

    # method to build a slug
    def slug(self):
        if self.has_valid_hire_date():
            slugstring = "{} {}".format(
                self.hire_date.strftime("%Y%m%d"),
                self.full_name()
            )
            return slugify(slugstring, to_lower=True)
        else:
            slugstring = "{} {} {}".format(
                self.agency_id,
                self.job_code,
                self.full_name()
            )
            return slugify(slugstring, to_lower=True)
        
    def __str__(self):
        return self.full_name()
        
        
def download_payroll_data():
    """Download payroll and lookup files."""
    
    # connect to the FTP server
    ftp = FTP(environ['OK_STATE_FTP_HOST'],
              environ['OK_STATE_FTP_USERNAME'],
              environ['OK_STATE_FTP_PASSWORD'])
    
    # get a list of the files
    files = ftp.nlst()

    # use regex to target payroll files
    target_years_regex = "".join([
        "(",
        str(FIRST_FISCAL_YEAR)[2:],
        "|",
        str(FIRST_FISCAL_YEAR+1)[2:],
        ")"
    ])

    pattern = re.compile("CALP" + target_years_regex + "\d{2}.DAT")
    payroll_files = [x.group(0) for q in files for x in [pattern.search(q)] if x]

    # loop over that list, downloading each file
    # ... checking first to see if it already exists
    for file in payroll_files:
        if file not in listdir("raw_data"):
            print('            ' + file)
            ftp.retrbinary('RETR ' + file,
                           open("raw_data/" + file, 'wb').write)

    # download the lookup files
    ftp.retrbinary('RETR AGCYINFO.DAT',
                   open("raw_data/agency_list.DAT", 'wb').write)
    ftp.retrbinary('RETR OBJCTCD.DAT',
                   open("raw_data/paycode_list.DAT", 'wb').write)

    # disconnect
    ftp.quit()


def in_fiscal_year(date_obj):
    """Does this date fall within the fiscal year?"""

    fiscal_start = date(FIRST_FISCAL_YEAR, 7, 1)
    fiscal_end = date(FIRST_FISCAL_YEAR+1, 6, 30)

    return fiscal_start <= date_obj <= fiscal_end
        

def get_date_obj(d):
    """Return a date object from a payroll record date string."""

    try:
        year = d[:4]
        month = d[4:6]
        day = d[6:8]
        return date(int(year), int(month), int(day))
    except:
        return date(1900, 1, 1)


def get_unique_ids(data_file, extra_var, slice_num):
    """Return a unique list of agency or payroll codes."""
        
    # Start with a list of codes
    # that have appeared in previous data sets but not
    # in the master file
    codes = extra_var
    
    # Then loop over the master file
    with open(data_file, "rb") as d:
        data = d.readlines()
        for row in data:
            d = {}
            code = str(row[:slice_num])
            name = row[slice_num:].strip()
            
            # a little name cleanup
            for item in GARBAGE_STRINGS:
                name = name.replace(*item)

            d['id'] = code
            d['name'] = name
            if not d in codes:
                codes.append(d)

    return codes


def parse_payroll_data():
    """Parse payroll files."""
    
    # get a list of agency codes
    agency_codes = get_unique_ids(
        "raw_data/agency_list.DAT",
        EXTRA_EDU_AGENCIES,
        3
    )
    
    agency_codes = [x["id"] for x in agency_codes]

    # get a list of payroll codes
    payroll_codes = get_unique_ids(
        "raw_data/paycode_list.DAT",
        EXTRA_PAYROLL_CODES,
        4
    )

    payroll_codes = [x["id"] for x in payroll_codes]

    # create lists to hold missing values
    missing_agency_codes = []
    missing_payroll_codes = []

    # open output files        
    with open("state-parsed-payroll-data.txt", "wb") as state_parsed, \
         open("edu-parsed-payroll-data.txt", "wb") as edu_parsed:
        
        # define the field names
        fieldnames = [
            'agency_id',
            'last',
            'rest',
            'full_name',
            'hire_date',
            'job_title',
            'amount',
            'pay_code',
            'name_slug'
        ]
        
        # create dictwriters
        state_writer = csv.DictWriter(state_parsed, fieldnames=fieldnames)
        edu_writer = csv.DictWriter(edu_parsed, fieldnames=fieldnames)
        
        # write the headers
        state_writer.writeheader()
        edu_writer.writeheader()
        
        # target the payroll files
        payroll_files = ["raw_data/" + x for x in listdir('raw_data') if re.search(r'^CALP\d{4}\.DAT$', x)]

        # raise an exception if there are no files to parse
        if len(payroll_files) == 0:
            raise IndexError("ain't no data files to whang on, so")

        # otherwise, loop over the files
        for payroll_file in payroll_files:
            print("        " + payroll_file)

            with open(payroll_file, "rb") as f:
                data = f.readlines()
                for row in data:
                    # create an instance of PayrollRecord class
                    pay_record = PayrollRecord(row)
                    
                    # only proceed if the amount is > 0
                    # and the payment date is in the target fiscal year
                    # and the last name isn't blank
                    if (pay_record.amount > 0.00 and
                            in_fiscal_year(pay_record.payment_date) and
                            pay_record.last_name != ""):
                        
                        # if the agency code isn't in the master list,
                        # add to the list of missing codes
                        if pay_record.agency_id not in agency_codes:
                            missing_agency_codes.append(pay_record.agency_id)

                        # ditto for payroll codes
                        if pay_record.pay_code not in payroll_codes:
                            missing_payroll_codes.append(pay_record.pay_code)
                            
                        record_to_write = {
                            'agency_id': pay_record.agency_id,
                            'last': pay_record.last_name,
                            'rest': pay_record.first_and_middle_name(),
                            'full_name': pay_record.full_name(),
                            'hire_date': pay_record.hire_date,
                            'job_title': pay_record.job_title,
                            'amount': pay_record.amount,
                            'pay_code': pay_record.pay_code,
                            'name_slug': pay_record.slug()
                        }
                    
                        # write to output files
                        if pay_record.is_education_employee():
                            edu_writer.writerow(record_to_write)
                        else:
                            state_writer.writerow(record_to_write)

    # log missing agency/pay records to file
    # (follow up on these with state data folks)
    if len(missing_agency_codes) > 0:
        with open("missing-agency-codes.txt", "wb") as missing_a:
            for code in missing_agency_codes:
                missing_a.write(code + "\n")

    if len(missing_payroll_codes) > 0:
        with open("missing-payroll-codes.txt", "wb") as missing_p:
            for code in missing_payroll_codes:
                missing_p.write(code + "\n")


def aggregate_payroll_data():
    """Roll through master salary files, group & aggregate."""
    
    state_out = open("state-ready-to-upload.txt", "wb")
    edu_out = open("edu-ready-to-upload.txt", "wb")

    # define the field names
    fieldnames = [
        'empty_str',
        'last_name',
        'rest_name',
        'full_name',
        'agency_id',
        'job_title',
        'hire_date',
        'total_pay',
        'another_empty_string',
        'fiscal_year',
        'slug',
        'show_hire_date',
        'a_third_empty_string'
    ]
    
    # create dictwriters
    state_writer = csv.DictWriter(state_out,
                                  fieldnames=fieldnames,
                                  delimiter='~',
                                  quotechar='"',
                                  quoting=csv.QUOTE_NONNUMERIC)

    edu_writer = csv.DictWriter(edu_out,
                                fieldnames=fieldnames,
                                delimiter='~',
                                quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)


    # create dataframes from parsed csvs
    # `keep_default_na=False` needed to handle
    # literal names like NULL and NA
    dataframes = {
        "state": pd.read_csv("state-parsed-payroll-data.txt",
                             dtype={'last': object,
                                    'rest': object,
                                    'agency_id': object,
                                    'pay_code': object,
                                    'job_code': object
                             },
                             keep_default_na=False),

        "higher-ed": pd.read_csv("edu-parsed-payroll-data.txt",
                                 dtype={'last': object,
                                        'rest': object,
                                        'agency_id': object,
                                        'pay_code': object,
                                        'job_code': object
                                 },
                                 keep_default_na=False),
    }

    # loop over each dataframe    
    for df in dataframes:    
        print "working on " + df + " records ..."

        # group by name slug
        for k, v in dataframes[df].groupby(['name_slug']):
            last_name = v['last'].tolist()[0]
            rest_name = v['rest'].tolist()[0]
            full_name = v['full_name'].tolist()[0]
            hire_date = v['hire_date'].tolist()[0]
            agency_id = v['agency_id'].tolist()[0]
            job_title = v['job_title'].tolist()[0]
            slug = k

            # get sum of amounts
            total_pay = v['amount'].sum()

            show_hire_date = "0"

            if df == "state":
                show_hire_date = "1"

            record_to_write = {
                'empty_str': '',
                'last_name': last_name,
                'rest_name': rest_name,
                'full_name': full_name,
                'agency_id': agency_id,
                'job_title': job_title,
                'hire_date': hire_date,
                'total_pay': str(total_pay),
                'another_empty_string': '',
                'fiscal_year': FIRST_FISCAL_YEAR,
                'slug': slug,
                'show_hire_date': show_hire_date,
                'a_third_empty_string': ''
            }

            if df == "state":
                state_writer.writerow(record_to_write)
            else:
                edu_writer.writerow(record_to_write)
        
    state_out.close()
    edu_out.close()

