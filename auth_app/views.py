from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.utils.timezone import datetime
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
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

        
