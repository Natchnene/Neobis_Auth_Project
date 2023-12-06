from django.shortcuts import render
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer
from .renderers import UserJSONRenderer


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

