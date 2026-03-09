from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user_app.Api.serializers import RegisterSerializer



@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email

            referesh = RefreshToken.for_user(account)
            data['token'] = {
                'refersh':str(referesh),
                'access':str(referesh.access_token)
            }
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)