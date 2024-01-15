from rest_framework import serializers
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    captcha = CaptchaField(read_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined', 'avatar']

