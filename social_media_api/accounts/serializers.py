from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login

# Use get_user_model() to dynamically reference the custom user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract password from the validated data
        
        # Create the user using create_user to ensure password is hashed
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Explicitly set the password to hash it
        user.save()

        # Create and return the token for the user
        token = Token.objects.create(user=user)
        return token

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        
        # If the user is authenticated and active, proceed
        if user and user.is_active:
            update_last_login(None, user)
            return user
        
        # Raise a validation error if authentication fails
        raise serializers.ValidationError("Invalid credentials")
