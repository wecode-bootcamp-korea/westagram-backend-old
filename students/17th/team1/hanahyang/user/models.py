from django.db   import models

class User(models.Model):
    email      = models.EmailField(max_length=50, unique=True) 
    name       = models.CharField(max_length=20, unique=True) 
    phone      = models.CharField(max_length=15, unique=True)
    password   = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='to_user')
    to_user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_user')
    
    class Meta:
        db_table = 'follow'
