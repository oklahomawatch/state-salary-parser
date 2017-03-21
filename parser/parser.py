from __future__ import print_function

from os import listdir
import re
import csv

import pandas as pd

import lookups
import utils
from models import PayrollRecord


def parse_payroll_data():
    """Parse payroll files."""

    # get a list of agency codes
    agency_codes = utils.get_unique_ids(
        '../raw_data/agency_list.DAT',
        lookups.EXTRA_EDU_AGENCIES,
        3
    ).keys()

    # get a list of payroll codes
    payroll_codes = utils.get_unique_ids(
        '../raw_data/paycode_list.DAT',
        lookups.EXTRA_PAYROLL_CODES,
        4
    ).keys()

    # create lists to hold any missing values
    missing_agency_codes = []
    missing_payroll_codes = []

    # open output files
    with open('../parsed_data/state-parsed-payroll-data.txt', 'w') as state_parsed, open('../parsed_data/edu-parsed-payroll-data.txt', 'w') as edu_parsed:  # NOQA

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
        payroll_files = ['../raw_data/' + x for x in listdir('../raw_data')
                         if re.search(r'^CALP\d{4}\.DAT$', x)]

        # raise an exception if there are no files to parse
        if len(payroll_files) == 0:
            raise IndexError('You need to download data before parsing.')

        # otherwise, loop over the files
        for payroll_file in payroll_files:
            print('        ' + payroll_file)

            with open(payroll_file, 'r') as f:
                data = f.readlines()
                for row in data:
                    # create an instance of PayrollRecord class
                    pay_record = PayrollRecord(row)

                    # only proceed if the amount is > 0
                    # and the payment date is in the target fiscal year
                    # and the last name isn't blank
                    if (pay_record.amount > 0.00 and
                            utils.in_fiscal_year(pay_record.payment_date) and
                            pay_record.last_name != ''):

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
        with open('../fixme/missing-agency-codes.txt', 'w') as missing_a:
            for code in missing_agency_codes:
                missing_a.write(code + '\n')

    if len(missing_payroll_codes) > 0:
        with open('../fixme/missing-payroll-codes.txt', 'w') as missing_p:
            for code in missing_payroll_codes:
                missing_p.write(code + '\n')


def aggregate_payroll_data():
    """Roll through master salary files, group & aggregate."""

    state_out = open('../parsed_data/state-personnel-ready-to-upload.txt', 'w')  # NOQA
    edu_out = open('../parsed_data/edu-personnel-ready-to-upload.txt', 'w')
    state_agency_out = open('../parsed_data/state-agencies-ready-to-upload.txt', 'w')   # NOQA
    edu_agency_out = open('../parsed_data/edu-agencies-ready-to-upload.txt', 'w')  # NOQA

    # get a list of agency codes
    agency_codes = utils.get_unique_ids(
        '../raw_data/agency_list.DAT',
        lookups.EXTRA_EDU_AGENCIES,
        3
    )

    # get a list of payroll codes
    payroll_codes = utils.get_unique_ids(
        '../raw_data/paycode_list.DAT',
        lookups.EXTRA_PAYROLL_CODES,
        4
    )

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
        'state': pd.read_csv('../parsed_data/state-parsed-payroll-data.txt',
                             dtype={
                                'last': object,
                                'rest': object,
                                'agency_id': object,
                                'pay_code': object,
                                'job_code': object
                             },
                             keep_default_na=False),

        'higher-ed': pd.read_csv('../parsed_data/edu-parsed-payroll-data.txt',
                                 dtype={
                                    'last': object,
                                    'rest': object,
                                    'agency_id': object,
                                    'pay_code': object,
                                    'job_code': object
                                 },
                                 keep_default_na=False),
    }

    # loop over each dataframe
    for df in dataframes:
        print('working on ' + df + ' personnel records ...')

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

            show_hire_date = '1'

            if hire_date == '1900-01-01':
                show_hire_date = '0'

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
                'fiscal_year': lookups.FIRST_FISCAL_YEAR,
                'slug': slug,
                'show_hire_date': show_hire_date,
                'a_third_empty_string': ''
            }

            if df == 'state':
                state_writer.writerow(record_to_write)
            else:
                edu_writer.writerow(record_to_write)

        print('working on ' + df + ' agency records ...')

        agency_file_dict = {}
        for k, v in dataframes[df].groupby(['agency_id', 'pay_code']):
            agency_id = k[0]
            agency = agency_codes.get(agency_id, None)
            pay_code = k[1]
            payroll_name = payroll_codes.get(pay_code, None)
            total_pay = v['amount'].sum()
            payroll_str = ':'.join([payroll_name, str(total_pay)])

            agency_dict = agency_file_dict.get(agency_id, None)

            if agency_dict:
                agency_file_dict[agency_id]['payroll'].append(payroll_str)
                agency_file_dict[agency_id]['total'] += total_pay
            else:
                agency_file_dict[agency_id] = {}
                agency_file_dict[agency_id]['name'] = agency
                agency_file_dict[agency_id]['total'] = 0.0
                agency_file_dict[agency_id]['payroll'] = []

        for agency in agency_file_dict:
            outlist = [
                agency,
                agency_file_dict[agency]['name'],
                str(agency_file_dict[agency]['total']),
                '|'.join(agency_file_dict[agency]['payroll'])
            ]

            if df == 'state':
                state_agency_out.write('~'.join(outlist) + '\n')
            else:
                edu_agency_out.write('~'.join(outlist) + '\n')

    state_out.close()
    edu_out.close()
    state_agency_out.close()
    edu_agency_out.close()


if __name__ == '__main__':
    utils.download_payroll_data()
    parse_payroll_data()
    aggregate_payroll_data()
