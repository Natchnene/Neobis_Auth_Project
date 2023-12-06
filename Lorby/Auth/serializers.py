from rest_framework import serializers

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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)
    tokens = serializers.SerializerMethodField()


