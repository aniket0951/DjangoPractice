from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import (
                                FileExtensionValidator, 
                                MaxValueValidator,
                                MinValueValidator
                            )
# Create your models here.

class MyBaseModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    name = models.CharField(max_length=255)

    email = models.CharField(max_length=255, unique=False)

    password = models.CharField(max_length=56,
                                blank=False, null=False)                                             

class UserAddress(MyBaseModel):
    area = models.CharField(max_length=255,
                            blank=False, null=False)

    address_line = models.CharField(max_length=255,
                            blank=False, null=False)

    pincode_number = models.PositiveIntegerField(
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
        blank=False,
        null=False) 
                                               

class Places(MyBaseModel):
    place_name = models.CharField(max_length=63,
                                   blank=False, null=False)

    place_address = models.CharField(max_length=255,
                                     blank=False, null=False)           

    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             blank=False, null=False)                                                                                     