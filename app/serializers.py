from rest_framework import serializers
from .models import *
from rest_auth.registration.serializers import RegisterSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'url')


class ProfileSerializer(RegisterSerializer):
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    location = serializers.CharField(required=True)
    role = serializers.BooleanField()

    def custom_signup(self, request, user):
        profile = Profile()
        params = request._data
        user = User()
        user.email = params.get('email', '')
        user.username = params.get('username', '')
        user.first_name = params.get('first_name', '')
        user.last_name = params.get('last_name', '')
        user.save()
        user.set_password(params.get('password1', ''))
        user.save()
        profile.location = params.get('location', '')
        profile.role = params.get('role', '')
        profile.user = user
        profile.save()
        return profile


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    freelancer = serializers.ReadOnlyField(source='freelancer.email')
    freelancer_name = serializers.CharField(source='freelancer.get_username', read_only=True)

    class Meta:
        model = Offer
        fields = ('delivery_time', 'price', 'details', 'project', 'freelancer', 'freelancer_name',)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    offers = OfferSerializer(many=True, read_only=True)
    employer = serializers.ReadOnlyField(source='employer.email')
    employer_name = serializers.CharField(source='employer.get_username', read_only=True)
    location = serializers.ChoiceField(choices=LOCATION_CHOICES)
    publish_date = serializers.DateTimeField(format='%d/%m/%Y, %H:%M', read_only=True)

    class Meta:
        model = Project
        fields = ('title', 'description', 'location', 'publish_date', 'budget', 'category', 'category_name', 'offers', 'employer', 'employer_name', 'url',)