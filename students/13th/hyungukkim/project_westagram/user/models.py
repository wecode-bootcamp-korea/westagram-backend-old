from django.db import models

class Account(models.Model):
	name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	phone = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	followers = models.IntegerField(default=0)
	followees = models.IntegerField(default=0)

	relations = models.ManyToManyField('self', symmetrical=False, through='Relation', related_name='+')

class Relation(models.Model):
	from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='relation_from_account')
	to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='relation_to_account')
