from rest_framework import serializers
from operations import models as om
from accounts import models as am


class FarmSerializer(serializers.ModelSerializer):
    owner_profile = am.FarmerProfile

    class Meta:
        model = om.Farm
        fields = ['id', 'name', 'address',
                  'description', 'size', 'owner_profile',
                  'created']


class OfferingSerializer(serializers.ModelSerializer):
    owner_profile = am.MerchantProfile

    class Meta:
        model = om.Offering
        fields = ['id', 'name', 'description',
                  'type', 'owner_profile', 'created']


class VisitationSerializer(serializers.ModelSerializer):
    officer = am.User
    farmer = am.User
    farm = om.Farm

    class Meta:
        model = om.Visitation
        fields = ['id', 'officer', 'farmer', 'farm',
                  'summary', 'created']
