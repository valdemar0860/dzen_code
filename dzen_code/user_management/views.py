from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import UserSerializer


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user:
            response = super().post(request, *args, **kwargs)
            refresh = response.data.get("refresh")
            access = response.data.get("access")

            return Response({"access_token": access, "refresh_token": refresh}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        avatar = request.data.get('avatar')

        if CustomUser.objects.filter(email=email).exists():
            return Response({'detail': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser(email=email, avatar=avatar)
        user.set_password(password)
        user.save()

        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
