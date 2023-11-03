from rest_framework import serializers
from .models import UserProfile, ChildrensHome, Donation, Visit,Review

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.Serializer):
   class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Please provide both username and password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        attrs['token'] = JWTAuthentication().get_token(user)

        return attrs
class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password'),
        }

        if not all(credentials.values()):
            raise serializers.ValidationError('Please provide both username and password')

        user = authenticate(**credentials)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if user.role != 'USER':
            raise serializers.ValidationError('You are not allowed to access this endpoint')

        return {
            'user': user,
            'token': super().validate(attrs),
        }

class ChiefJWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password'),
        }

        if not all(credentials.values()):
            raise serializers.ValidationError('Please provide both username and password')

        user = authenticate(**credentials)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if user.role != 'CHIEF':
            raise serializers.ValidationError('You are not allowed to access this endpoint')

        return {
            'user': user,
            'token': super().validate(attrs),
        }


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'name', 'email']

class ChildrenHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildrensHome
        fields = ['id', 'name', 'address', 'mission', 'vision', 'values', 'programs', 'needs']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'amount', 'date', 'user', 'children_home']

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'date', 'user', 'children_home']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comments', 'user', 'children_home']