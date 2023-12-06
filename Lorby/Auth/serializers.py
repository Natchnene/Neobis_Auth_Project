from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib import auth

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)
    password_check = serializers.CharField(min_length=8, max_length=15, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain only alphabetic characters.',
        'password_mismatch': 'The two password fields did not match.'
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']

    def validate(self, data):
        username = data.get('username', '')

        if not username.isalpha():
            raise serializers.ValidationError(
                self.default_error_messages['username']
            )

        if data['password'] != data ['password_check']:
            raise serializers.ValidationError(
                self.default_error_messages['password_mismatch']
            )

        return data

    def create(self, validated_data):
        validated_data.pop('password_check', '')
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])

        return{
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Email is not verified')

        return {
            'username': user.email,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

