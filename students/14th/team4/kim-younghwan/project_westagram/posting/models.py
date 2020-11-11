from django.db import models

class Broads(models.Model):
    title               = models.CharField(max_length=200)
    created_date        = models.DateTimeField(auto_now =True)
    photo               = models.ImageField(blank=True)
    name                = models.ForeignKey('user.Accounts',on_delete = models.CASCADE)
    created             = models.DateTimeField(auto_now=True)
    updated             = models.DateTimeField(auto_now_add=True)        


class Comments(models.Model):
    name                = models.ForeignKey('user.Accounts',on_delete=models.CASCADE)
    broad               = models.ForeignKey('Broads',on_delete=models.CASCADE)
    content             = models.TextField(null=True)
    created             = models.DateTimeField(auto_now=True)
    updated             = models.DateTimeField(auto_now_add=True) 



    