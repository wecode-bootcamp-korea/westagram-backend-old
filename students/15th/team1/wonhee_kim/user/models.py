from django.db import models


class User(models.Model):
	"""
	사용자 정보를 저장하는 테이블
	"""
	name                = models.CharField(max_length=30, null=True)
	nick_name           = models.CharField(max_length=30, null=True)
	hashed_password     = models.CharField(max_length=255)
	email               = models.CharField(max_length=100, null=True)
	phone_number        = models.CharField(max_length=11, null=True)
	follow              = models.ManyToManyField("self", through='Follow', symmetrical=False)
	created_at          = models.DateTimeField(auto_now_add=True)
	password_changed_at = models.DateTimeField(null=True)

	class Meta:
		db_table = 'users'

	def __str__(self):
		return self.name


class Follow(models.Model):
	from_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='from_user')
	to_user   = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='to_user')

	class Meta:
		unique_together = ('from_user', 'to_user')
		db_table        = 'follows'
