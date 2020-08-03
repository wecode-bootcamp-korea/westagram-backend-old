from django.db import models


class Post(models.Model):
   name       = models.ForeignKey('User.User', on_delete = models.CASCADE)
   image      = models.URLField(max_length = 2000)
   content    = models.CharField(max_length = 200)
   created_at = models.DateTimeField(auto_now_add = True)
  
   class Meta:
       db_table = 'post'

   def __str__(self):
       return self.name
    
