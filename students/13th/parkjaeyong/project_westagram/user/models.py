from django.db import models

class Users(models.Model):
    name         = models.CharField(max_length=30)
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password     = models.IntegerField()
    

    class Meta:
        db_table='user'





# 생성한 사용자 클래스를 불러옵니다. 한 번에 모든 클래스를 import 해서는 안됩니다. 내가 사용할 클래스를 정확히 지칭해주세요
# 인스타그램에 회원가입 할 때에는 전화번호, 사용자 이름 또는 이메일이 필수로 필요합니다.
# 인스타그램에 회원가입 할 때에는 비밀번호도 필수로 필요합니다.
# 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
# 회원가입시 이메일을 사용할 경우, 이메일에는 @와 .이 필수로 포함되어야 합니다. 해당 조건이 만족되지 않을 시 적절한 에러를 반환해주세요. 이 과정을 email validation이라고 합니다.
# 회원가입시 비밀번호는 8자리 이상이어야만 합니다. 해당 조건이 만족되지 않을 시, 적절한 에러를 반환해주세요. 이 과정을 password validation이라고 합니다.
# 회원가입시 서로 다른 사람이 같은 전화번호나 사용자 이름, 이메일을 사용하지 않으므로 기존에 존재하는 자료와 중복되어서는 안됩니다. 적절한 에러를 반환해주세요.
# 회원가입이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
# [추가 구현 사항] -> email validation 또는 password validation 과정에서 정규식을 사용해보세요.
