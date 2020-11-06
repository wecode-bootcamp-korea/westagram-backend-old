import re
from user.const import REGEX_EMAIL, PHONE_NUM_LEN, NONE

class Validation:
    
    @staticmethod
    def is_not_blank(*args):
        for value in args:
            if value == "" or value == NONE:
                return False
            else:
                return True
    
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
    
    @staticmethod
    def is_valid_object(user_object):
        if user_object is not NONE:
            return True
        else:
            return False