from django.db import models


class User(models.Model):
    name         = models.CharField(max_length=20)
    user_name    = models.CharField(max_length=20)
    email        = models.EmailField(max_length=30)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    relationship = models.ManyToManyField('self', through='Relationship',
                                          symmetrical=False,
                                          )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'User'


class Relationship(models.Model):
    from_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='to_user')

    def __str__(self):
        return f'{self.from_user}:{self.to_user}'

    class Meta:
        db_table = 'Relationship'
