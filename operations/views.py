from django.shortcuts import render
from rest_framework import views, viewsets
from operations import models as om
from operations import serializers as os

# Create your views here.


class FarmViewSet(viewsets.ModelViewSet):

    queryset = om.Farm.objects.all()
    serializer_class = os.FarmSerializer


class OfferingViewSet(viewsets.ModelViewSet):

    queryset = om.Offering.objects.all()
    serializer_class = os.OfferingSerializer


class VisitationViewSet(viewsets.ModelViewSet):

    queryset = om.Visitation.objects.all()
    serializer_class = os.VisitationSerializer
