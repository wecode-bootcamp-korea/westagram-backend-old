from django.db import models

class User(models.Model):
    # username = models.CharField(max_length=20, verbose_name='사용자명',unique=True, null=True)
    password = models.CharField(max_length=20, verbose_name='비밀번호')
    # mobile   = models.CharField(max_length=20, verbose_name='휴대폰', null=True)
    email    = models.CharField(max_length=30, verbose_name='이메일',unique=True)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table            = 'users'
        verbose_name        = 'user'
        verbose_name_plural = 'user'
        ordering            = ('email',)

