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
