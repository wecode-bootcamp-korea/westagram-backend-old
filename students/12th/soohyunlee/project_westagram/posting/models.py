from django.db   import models
from user.models import User

class Posting(models.Model):

    writer        = models.ForeignKey(User, on_delete=models.CASCADE)
    contents      = models.TextField(max_length=300, null=True)
    img_url       = models.ImageField(null=True)
    created_at    = models.DateTimeField(auto_now_add=True, null=True)
    updated_at    = models.DateTimeField(auto_now = True, null=True)

    def __str__(self):
        return str(self,writer)
    class Meta:
        db_table='posting'