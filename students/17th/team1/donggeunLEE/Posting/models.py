from django.db import models

# Create your models here.

class UserPosting(models.Model):
    user_ID    = models.ForeignKey('User.Userinfo', on_delete=models.SET_NULL, null=True)
    create_at  = models.DateTimeField(auto_now=True)
    image_url  = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.user_ID.name}'

    class Meta:
        db_table =  'userposting'
