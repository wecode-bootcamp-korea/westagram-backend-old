import uuid

from django.db import models

class User(models.Model):
    uuid           = models.UUIDField(
        primary_key = True, 
        default     = uuid.uuid4, 
        editable    = False
    )
    phone_or_email = models.CharField(
        max_length  = 64, 
        null        = False, 
        blank       = False, 
        unique      = True,
        editable    = False,
    )
    name           = models.CharField(
        max_length  = 32, 
        null        = False, 
        blank       = False,
        editable    = False,
    )
    username       = models.CharField(
        max_length  = 32, 
        null        = False, 
        blank       = False, 
        unique      = True,
        editable    = False,
    )
    password       = models.CharField(
        max_length  = 256, 
        null        = False,
        blank       = False
    )
    created_at     = models.DateTimeField(
        auto_now_add = True, 
        editable     = False
    )
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
