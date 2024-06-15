from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AuthToken
from django.utils.timezone import datetime
class CustomAuthToken(BaseAuthentication):
    TOKEN=['bearer','token']
    def authenticate(self, request):
        """
        Custom authentication class
        """
        token=request.headers.get('Authorization','')
        token=token.split()

        if not token or len(token)!=2:
            return None
        if token[0].lower() not in self.TOKEN:
            return None
        
        token=AuthToken.objects.filter(
            access_token=token[1],
            access_tok_valid__gt=datetime.now()
            ).first()
        
        if token is None:
            raise AuthenticationFailed('Invalid Token')
        return (token.user,None)

        
        
        