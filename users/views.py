from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)  ## biz sinyal kullanarak bu tokeni kaydettik zaten şimdi burada çağırarak  token değişkenine aldık 
        data = serializer.data 
        data["key"] = token.key  ## ve api isteği yapan kişiye buradan tokeni de dönmek için serializer data içine tokeni de ekledik ki artık tokeni görebilsin
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    