from typing import Iterable
from django.db import models
from datetime import timedelta
from django.utils.timezone import datetime  
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
# Create your models here.
class AuthToken(models.Model):
    
    class Meta:
        db_table='AuthToken'
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    refresh_token=models.CharField(max_length=250,default='')
    refresh_tok_valid=models.DateTimeField(null=True)
    access_token=models.CharField(max_length=250)
    access_tok_valid=models.DateTimeField(null=True)
    
    def save(self, **kwargs) -> None:
        self.access_token=default_token_generator.make_token(self.user)
        if self.access_token==self.refresh_token:
            self.access_token=default_token_generator.make_token(self.user)
        self.access_tok_valid=datetime.now()+timedelta(minutes=15)
        return super().save(**kwargs)

class ResetPasswordToken(models.Model):
    class Meta:
        db_table='ResetToken'

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    reset_token=models.CharField(max_length=250)
    
    def save(self, **kwargs) -> None:
        self.reset_token=default_token_generator.make_token(self.user)
        return super().save(**kwargs)

