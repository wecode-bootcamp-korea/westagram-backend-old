import re
import bcrypt

from user.const import REGEX_EMAIL, PHONE_NUM_LEN, NONE, UTF8

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
    
    @staticmethod
    def is_valid_password(password, hashed_password):
        if bcrypt.checkpw(password.encode(UTF8), hashed_password):
            return True
        else:
            return False