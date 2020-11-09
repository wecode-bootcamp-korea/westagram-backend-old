from django.db import models
# import user.models as user

class Posting(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    time = models.DateField(auto_now=True)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'postings'
