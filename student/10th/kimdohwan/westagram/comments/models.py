from django.db import models
from core import models as core_models

class Comment(core_models.TempDate):
    userid = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=300, default="")

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.userid
