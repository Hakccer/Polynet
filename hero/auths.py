from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken, Token
from rest_framework.response import Response
from django.contrib.auth.models import User


class CustomObtainToken(ObtainAuthToken):
    def post(self, request):
        my_serializer = self.serializer_class(
            data=request.data, context={'request': request})
        my_serializer.is_valid(raise_exception=True)
        my_user = my_serializer.validated_data['user']
        tokens, created = Token.objects.get_or_create(user=my_user)
        return Response({
            'token': tokens.key,
            'user_id': my_user.pk,
            'mailer': my_user.email
        })
