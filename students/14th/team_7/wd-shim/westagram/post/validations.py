import re
from user.const import REGEX_EMAIL, PHONE_NUM_LEN

class Validation:
    
    @staticmethod
    def is_blank(*args):
        return not all([value for value in args])
    
    @staticmethod
    def is_valid_email(email):
        return re.search(REGEX_EMAIL, email)
    
    @staticmethod
    def is_valid_phone_number(phone):
        return phone.isdecimal() and len(phone) == PHONE_NUM_LEN