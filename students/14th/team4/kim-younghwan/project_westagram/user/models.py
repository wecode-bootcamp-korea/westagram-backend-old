from django.db import models

class Accounts(models.Model):
        email           = models.EmailField(max_length=50)
        name            = models.CharField(max_length=50)
        password        = models.CharField(max_length = 300)
        created_at      = models.DateTimeField(auto_now_add = True)
        updated_at      = models.DateTimeField(auto_now = True)

        class Meta:
                db_table = 'accounts'

class Broadlikes(models.Model):
        account         = models.ForeignKey('Accounts', on_delete=models.CASCADE, null=True)
        broad           = models.ForeignKey('posting.Broads', on_delete=models.CASCADE,null=True)
        
        class Meta:
                db_table = 'accounts_borads'



