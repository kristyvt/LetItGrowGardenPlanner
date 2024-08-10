'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

validate handles data validation of
integers, float, text, and date data types
Last Revised 8/3/24
'''

import re
import datetime
from datetime import datetime


# class to validate data input by user
# or retrieved from the database
class Validate:
    def __init__(self, data):
        self.data = data  # the data to validate

    # function to validate any integer
    def validate_int(self):

        # if there is data, validate it
        if self.data:

            # check if integer
            try:
                int(self.data)
                return True

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None

    def validate_positive_int(self):
        # if there is data, validate it
        if self.data:
            print(self.data)
            try:
                # check if integer and if so, is it more than 0?
                int_data = int(self.data)
                if int_data > 0:
                    return True
                else:
                    return False

            except TypeError:
                return False

            except ValueError:
                return False

        # if no data, return null value
        else:
            return False

    def validate_positive_float(self):

        # if there is data, validate it
        if self.data:

            # check if float and if so, is it 0 or more?
            try:
                float_data = float(self.data)

                if float_data >= 0:
                    return True
                else:
                    return False

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None

    def validate_text(self):

        # if there is data, validate it
        if self.data:
            try:
                # test if string
                str(self.data)

                # set list of valid characters
                valid_chars = re.compile(r"[A-Za-z0-9\- _',:%&()]+")

                # set list of "dangerous" database strings
                invalid_strings = re.compile(r"[Dd][Rr][Oo][Pp] .+"
                                             r"|[Aa][Ll][Tt][Ee][Rr] .+"
                                             r"|[Dd][Ee][Ll][Ee][Tt][Ee] .+")

                # test if characters in string are valid
                if re.fullmatch(valid_chars, str(self.data)) and not re.fullmatch(invalid_strings, str(self.data)):
                    return True
                else:
                    return False

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None

    def validate_date(self):

        # if there is data, validate it
        if self.data:
            try:

                print(self.data)
                # test if date
                # first convert input to string
                data_string = str(self.data)

                # then attempt to convert the inputs string a date
                test_date = datetime.strptime(data_string,
                                              '%m/%d/%y').date()

                # return true if conversion is successful
                if test_date:
                    return True

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None
