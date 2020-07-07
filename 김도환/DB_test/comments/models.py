from django.db import models
from core import models as core_models
from user.models import User


class Comment(core_models.TempDate):
    userid = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=300, default="")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.userid
