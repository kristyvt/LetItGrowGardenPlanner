import re

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
            try:
                # check if integer and if so, is it 0 or more?
                int(self.data)
                if self.data >= 0:
                    return True
                else:
                    return False

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None

    def validate_positive_float(self):

        # if there is data, validate it
        if self.data:

            # check if float and if so, is it 0 or more?
            try:
                float(self.data)
                if self.data >= 0:
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
                valid_chars = re.compile(r"[A-Za-z0-9\- _',]+")

                # test if characters in string are valid
                if re.fullmatch(valid_chars, str(self.data)):
                    print(f"'{self.data}' is a valid string!")
                    return True
                else:
                    print(f"'{self.data}' is not a valid string!")
                    return False

            except ValueError:
                return False

        # if no data, return null value
        else:
            return None



# test code

data = 1
validated_data = Validate(data)
if validated_data.validate_text():
    print(validated_data.data)
elif validated_data.validate_text() == False:
    print('invalid data')
else:
    print('no data')
