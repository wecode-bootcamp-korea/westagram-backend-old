class BlankFieldException(Exception):
    def __init__(self):
        super().__init__('BlankFieldException')

class PasswordValidException(Exception):
    def __init__(self):
        super().__init__('PasswordValidException')

class AlreadyExistException(Exception):
    def __init__(self):
        super().__init__('AlreadyExistException')

class PostUploadFailException(Exception):
    def __init__(self):
        super().__init__('PostUploadFailException')

class ImageUploadFailException(Exception):
    def __init__(self):
        super().__init__("ImageUploadFailException")

class FailToGetKeysException(Exception):
    def __init__(self):
        super().__init__("FailToGetKeysException")