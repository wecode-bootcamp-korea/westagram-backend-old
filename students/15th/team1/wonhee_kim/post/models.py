from django.db import models

from user.models import User


class Post(models.Model):
	"""
	포스팅을 저장하는 테이블
	"""
	user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
	content    = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image_url  = models.CharField(null=True, max_length=2000)
	update_at  = models.DateTimeField(null=True)

	class Meta:
		db_table = 'posts'

	def __str__(self):
		return str(self.user.name) + "의 " + "post" + " / id" + "(" + self.id + ")"


class Comment(models.Model):
	"""
	포스트에 달리는 댓글을 저장하는 테이블
	"""
	post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
	user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
	content    = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)

	class Meta:
		db_table = 'comments'

	def __str__(self):
		return "포스트 " + str(self.post.id) + "에 대한 " + str(self.user.name) + "님의 댓글 " + str(self.id)
