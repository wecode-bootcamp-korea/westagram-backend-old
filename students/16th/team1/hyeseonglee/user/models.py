from django.db import models

class User(models.Model):
    password = models.CharField(max_length=20, verbose_name='비밀번호')
    email    = models.CharField(max_length=30, verbose_name='이메일',unique=True)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table            = 'users'
        verbose_name        = 'user'
        verbose_name_plural = 'user'
        ordering            = ('email',)

