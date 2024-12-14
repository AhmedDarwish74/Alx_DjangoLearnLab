from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login

# Dynamically reference the custom user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract password
        user = User.objects.create_user(**validated_data)  # Create user with password hashing
        user.set_password(password)  # Explicitly set the password to hash it (create_user does this internally)
        user.save()

        # Create a token for the new user
        token, created = Token.objects.get_or_create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Authenticate the user using provided credentials
        user = authenticate(**data)
        if user and user.is_active:
            # Generate a new token if authentication is successful
            token, created = Token.objects.get_or_create(user=user)
            update_last_login(None, user)  # Update last login time
            return {
                'token': token.key  # Return the token key
            }
        raise serializers.ValidationError("Invalid credentials")
