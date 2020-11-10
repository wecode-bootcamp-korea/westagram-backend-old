class BlankFieldException(Exception):
    def __init__(self):
        super().__init__('필수입력 항목을 작성해주세요.')

class EmailFormatException(Exception):
    def __init__(self):
        super().__init__('올바른 이메일 형식이 아닙니다.')

class PhoneFormatException(Exception):
    def __init__(self):
        super().__init__('올바른 전화번호 형식이 아닙니다.')

class PasswordFormatException(Exception):
    def __init__(self):
        super().__init__('올바른 비밀번호 형식이 아닙니다.')

class AlreadyExistException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 정보입니다.')

class AuthenticationException(Exception):
    def __init__(self):
        super().__init__('비밀번호가 일치하지 않습니다. 다시 확인하여 주세요.')