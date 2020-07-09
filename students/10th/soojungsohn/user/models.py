from django.db import models

class User(models.Model):
    name        = models.CharField(max_length = 50)
    email       = models.CharField(max_length = 50)
    password    = models.CharField(max_length = 300)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    main_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    sub_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_user')  
    status      = models.CharField(max_length = 50)

    class Meta:
        db_table = 'follows'

