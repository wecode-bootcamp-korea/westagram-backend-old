from django.db      import models
from django.conf    import settings

class Posting(models.Model):
    post_id      = models.ForeignKey('user.User',on_delete=models.CASCADE)
    post_url     = models.URLField(max_length= 300)
    description  = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'postings'