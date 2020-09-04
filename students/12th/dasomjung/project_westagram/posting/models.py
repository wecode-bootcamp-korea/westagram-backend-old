from django.db import models

class Posting(models.Model):
    writer         = models.ForeignKey('user.Users', on_delete=models.CASCADE) 
    # ForeignKey가 바라보는 값이 삭제되면 같이 삭제됨 설정
    contents       = models.TextField(max_length=500, null=True)
    published_date = models.DateTimeField('date published')  # auto_now_add 가 나을지?
    images_url     = models.ForeignKey('Images', on_delete=models.CASCADE)

class Images(models.Model):
    images_url = models.URLField(max_length=200)
    
