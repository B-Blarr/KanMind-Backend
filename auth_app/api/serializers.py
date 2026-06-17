"""Serializers for authentication: registration, login and user profiles."""

from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile model (tutorial leftover)."""

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration input and create a new user account."""

    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(max_length=60)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password':{
                'write_only': True
            }
        }

    def save(self):
        """Create the user (fullname->first_name, email->username) and hash pw."""
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'password downt match'})

        account = User(
            email=self.validated_data['email'], 
            username=self.validated_data['email'],
            first_name=self.validated_data['fullname'])
        account.set_password(pw)
        account.save()
        return account
        

    def validate_email(self, value):
        """Reject the email if a user with it already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
class LoginSerializer(serializers.Serializer):
    """Authenticate a user by email and password."""
        
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        

    def validate(self, data):
        """Authenticate the credentials and stash the user in the data."""
        user = authenticate(
            username=data['email'],     
            password=data['password'],)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user             
        return data