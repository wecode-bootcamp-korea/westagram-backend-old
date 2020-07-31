from django.db      import models

class User(models.Model):
    email      = models.EmailField(max_length = 100)
    password   = models.CharField(max_length = 100)
    follow     = models.ManyToManyField('self', through = 'follow', related_name = 'user')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    follow_user   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'follow_user')
    followee_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'followee_user')

    class Meta:
        db_table = 'follows'
