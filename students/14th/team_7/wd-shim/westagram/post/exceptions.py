class BlankFieldException(Exception):
    def __init__(self):
        super().__init__('값이 비어있습니다.')

class PasswordValidException(Exception):
    def __init__(self):
        super().__init__('올바른 비밀번호 형식이 아닙니다.')

class AlreadyExistException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 정보입니다.')