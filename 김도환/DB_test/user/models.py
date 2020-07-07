from django.db import models
from core import models as core_models


class User(core_models.TempDate):
    userid = models.CharField(max_length=30, default="")
    name = models.CharField(max_length=50, default="", null=False)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=300, default="", null=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name


# select * from user
# insert into user_user(name,email,password,created_at,updated_at) values("김도환","ehghksvjscl@nate.com","admin","2020-10-10","2020-10-10")
# http -v http://127.0.0.1:8000/ userid="ehghks1" name="김도환" email="ehghks1@naver.com" password="1234"
