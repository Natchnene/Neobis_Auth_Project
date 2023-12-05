from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain only alphabetic characters'
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalpha():
            raise serializers.ValidationError(
                self.default_error_messages
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
