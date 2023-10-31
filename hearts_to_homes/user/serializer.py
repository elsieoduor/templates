from rest_framework import serializers
from .models import UserProfile, ChildrensHome, Donation, Visit,Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email']

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