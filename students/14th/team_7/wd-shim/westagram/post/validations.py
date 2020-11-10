import re
from user.const import REGEX_EMAIL, PHONE_NUM_LEN, NONE

class Validation:
    
    @staticmethod
    def is_blank(*args):
        return not all([value for value in args])
    
    @staticmethod
    def is_valid_email(email):
        if re.search(REGEX_EMAIL, email):
            return True
        else:
            return False
    
    @staticmethod
    def is_valid_phone_number(phone):
        if phone.isdecimal() and len(phone) == PHONE_NUM_LEN:
            return True
        else:
            return False