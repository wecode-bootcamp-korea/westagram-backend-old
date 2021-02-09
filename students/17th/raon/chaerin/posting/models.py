from django.db    import models

from user.models  import Account

# Create your models here.

class Post(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_at = models.TimeField(auto_now_add = True, null=True)
    content    = models.TextField()
    image_url  = models.URLField()

    #def __str__(self):
     #   return self.user

    class Meta:
        db_table = 'posts'

