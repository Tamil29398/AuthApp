from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.utils.timezone import datetime
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import AuthToken,ResetPasswordToken
from datetime import timedelta
# Create your views here.

class AuthView(APIView):
    """
    Generate auth token and refresh token 
    """
    def post(self,request):
        """
        {username,password}
        """
        data=request.data
        user=authenticate(**data)
        if user is None:
            return Response('User Account Not Found',status=401)
        
        token,_=AuthToken.objects.get_or_create(user=user)
        token.refresh_token = default_token_generator.make_token(user)
        token.refresh_tok_valid=datetime.now()+timedelta(days=1)
        token.save()
        return Response({
            'access':token.access_token,
            'refresh':token.refresh_token
            })
class RefreshTokenView(APIView):
    def post(self,request):
        refresh_token=request.data.get('refresh','')
        token=AuthToken.objects.filter(refresh_token=refresh_token,refresh_tok_valid__gt=datetime.now()).first()
        if token is None:
            return Response('Invalid Authentication',status=401)
        token.save()
        return Response({'access':token.access_token})
        
class PasswordResetTokenView(APIView):
    def get(self,request):
        email=request.GET.get('email','')
        if not email:
            return Response('Email-id Requird')
        user=User.objects.filter(email=email).first()
        if user is None:
            return Response('User Account not Found',status=400)
        reset_token,_=ResetPasswordToken.objects.get_or_create(user=user)
        reset_token.save()
        return Response({
            'reset_token':reset_token.reset_token
        })
        
    def post(self,request):
        reset_token=request.data.get('reset_token','')
        password=request.data.get('password')

        user=ResetPasswordToken.objects.filter(reset_token=reset_token).first()
        if user is None:
            return Response('Invalid Token')
        user.user.set_password(password)
        user.user.save()
        return Response({'reset_password SuccessFully'})
    
    

