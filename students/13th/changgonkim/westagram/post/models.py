from django.db import models
from account.models import Account

class Posting(models.Model):
	poster		= models.ForeignKey(Account, on_delete=models.CASCADE)
	imageurl	= models.CharField(max_length=2000)
	caption		= models.CharField(max_length=500)
	create_time	= models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'posting'