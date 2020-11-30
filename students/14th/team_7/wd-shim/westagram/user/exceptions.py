class BlankFieldException(Exception):
    def __init__(self):
        super().__init__('BlankFieldException')

class EmailFormatException(Exception):
    def __init__(self):
        super().__init__('EmailFormatException')

class PhoneFormatException(Exception):
    def __init__(self):
        super().__init__('PhoneFormatException')

class PasswordFormatException(Exception):
    def __init__(self):
        super().__init__('PasswordFormatException')

class AlreadyExistException(Exception):
    def __init__(self):
        super().__init__('AlreadyExistException')

class WrongPasswordException(Exception):
    def __init__(self):
        super().__init__('WrongPasswordException')