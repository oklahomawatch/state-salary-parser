from datetime import date

from slugify import slugify

from utils import get_date_obj
from lookups import EDU_AGENCIES, EDU_TITLES


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
        return (str(self.agency_id) in EDU_AGENCIES or
                self.job_title.upper() in EDU_TITLES)

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
