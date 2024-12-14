from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token

# Use get_user_model() to dynamically reference the custom user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def create(self, validated_data):
        # Extract the password from the validated data
        password = validated_data.pop('password')
        
        # Create the user using the `create_user` method
        user = User.objects.create_user(**validated_data)
        
        # Set the password explicitly to ensure it's hashed
        user.set_password(password)
        
        # Save the user
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Use Django's authenticate function to check credentials
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        
        # Check if the user is valid and active
        if user and user.is_active:
            # Update the last login time
            update_last_login(None, user)
            return user
        
        # If authentication fails, raise a validation error
        raise serializers.ValidationError("Invalid credentials")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']
