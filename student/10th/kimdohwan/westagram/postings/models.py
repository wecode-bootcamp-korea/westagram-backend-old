from django.db import models
from core import models as core_models


class Posting(core_models.TempDate):
    userid = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    content = models.CharField(max_length=1000, default="")

    class Meta:
        db_table = "postings"

    def __str__(self):
        return self.title


class Comment(core_models.TempDate):
    userid = models.ForeignKey("user.User", on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, default="")

    class Meta:
        db_table = "comments"

    def __str__(self):
        return self.userid


class Love(core_models.TempDate):
    userid = models.ForeignKey("user.User", on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    loveTF = models.BooleanField(default=False)
