class BlankFieldException(Exception):
    def __init__(self):
        super().__init__('값이 비어있습니다.')

class PasswordValidException(Exception):
    def __init__(self):
        super().__init__('올바른 비밀번호 형식이 아닙니다.')

class AlreadyExistException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 정보입니다.')

class PostUploadFailException(Exception):
    def __init__(self):
        super().__init__('게시물이 정상적으로 생성하지 못했습니다.')

class ImageUploadFailException(Exception):
    def __init__(self):
        super().__init__("이미지가 업로드 되지 않았습니다.")