from django.db import models

class Users(models.Model):
    name = models.CharField(max_length = 45)
    nick_name = models.CharField(max_length = 45)
    email = models.EmailField(max_length = 10)
    phone = models.CharField(max_length = 13)
    password = models.CharField(max_length = 45)
    # profile_img = models.ImageField(
    #     upload_to='profile_img/', height_field = 250, width_field = 250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.id}, {self.name}"

    class Meta:
        db_table = 'users'