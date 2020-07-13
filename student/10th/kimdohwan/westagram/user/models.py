from django.db import models

from core import models as core_models

class User(core_models.TempDate):
    userid = models.CharField(max_length=30, default="")
    name = models.CharField(max_length=50, default="", null=False)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=300, default="", null=False)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

class Follow(core_models.TempDate):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="from_user_set")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="to_user_set")
    is_follow = models.BooleanField(default=False)

    class Meta:
        db_table = "follows"

    def __str__(self):
        return f"{self.from_user} - {to_user}"