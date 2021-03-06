import random
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import check_password

from accounts.serializers import (
    FarmerProfileSerializer, SignupSerializer, UserSerializer,
    SignInSerializer, MerchantProfileSerializer, ExtensionProfileSerializer,
    ActivateSerializer
)
from rest_framework.permissions import AllowAny

from accounts.models import FarmerProfile, User, MerchantProfile, ExtensionProfile
from accounts import constants as c
from accounts import utils as u

# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny

    # def get_queryset(self):
    #     return User.objects.all()
    #
    # def list(self, request, *args, **kwargs):
    #     merchants = User.objects.filter(user_type=c.MERCHANT)
    #     serializer = self.serializer_class(merchants, many=True)
    #
    #     return Response(
    #         {'data': serializer.data},
    #         status.HTTP_200_OK
    #     )
    #
    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     merchant = self.get_object()
    #     serializer = self.serializer_class(merchant)
    #
    #     return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], permission_classes=[AllowAny], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)

        url = "https://sms.nasaramobile.com/api/v2/sendsms"
        # url = "http://sms.nasaramobile.com/api"
        api_key = settings.SMS_KEY
        goona_id = "GOONACREDIT"

        if serializer.is_valid():
            user = serializer.save()
            if user is not None:
                pin = random.randint(1000000, 9999999)
                user.id_number = pin
                user.set_password(serializer.validated_data['password'])
                user.save()
                message = "You are welcome to GOONACREDIT. Your verification key is " + str(user.id_number)
                sms_response = u.send_sms(url, api_key, goona_id, user.phone_number, message)

                serializer = self.serializer_class(user)
                return Response(serializer.data, status.HTTP_201_CREATED)

    @action(methods=['POST'], permission_classes=[AllowAny], detail=False)
    def verify(self, request):
        serializer = ActivateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_verified = True
            Token.objects.get_or_create(user=user)

            serializer_data = UserSerializer(user)
            return Response(
                serializer_data.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['POST'], permission_classes=[AllowAny], detail=False)
    def signin(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            Token.objects.get_or_create(user=user)

            serialized_data = UserSerializer(user)
            return Response(
                serialized_data.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FarmerViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(user_type=c.FARMER)

    def list(self, request, *args, **kwargs):
        farmers = User.objects.filter(user_type=c.FARMER)
        serializer = self.serializer_class(farmers, many=True)

        return Response(
            {'data': serializer.data},
            status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        farmer = self.get_object()
        serializer = self.serializer_class(farmer)

        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], permission_classes=[AllowAny], detail=True)
    def create_profile(self, request, pk=None):
        user = self.get_object()
        address = request.data.get('address', None)
        family_size = request.data.get('family_size', None)
        credit = request.data.get('credit', None)
        profile = FarmerProfile.objects.create(
            user=user,
            address=address,
            family_size=int(family_size),
            credit_rating=int(credit)
        )
        serializer = FarmerProfileSerializer(profile)

        return Response(
            {
                'results': serializer.data
            },
            status.HTTP_201_CREATED
        )

    @action(methods=['POST'], permission_classes=[AllowAny], detail=True)
    def add_farm(self, request, pk=None):
        pass


class MerchantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(user_type=c.MERCHANT)

    def list(self, request, *args, **kwargs):
        merchants = User.objects.filter(user_type=c.MERCHANT)
        serializer = self.serializer_class(merchants, many=True)

        return Response(
            {'data': serializer.data},
            status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        merchant = self.get_object()
        serializer = self.serializer_class(merchant)

        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], permission_classes=[AllowAny], detail=True)
    def create_profile(self, request, pk=None):
        user = self.get_object()
        product = request.data.get('product')
        description = request.data.get('description')
        profile = MerchantProfile.objects.create(
            product=product,
            description=description,
            user=user
        )

        serializer = MerchantProfileSerializer(profile)
        return Response(
            {
                'data': serializer.data
            },
            status.HTTP_201_CREATED
        )


class ExtensionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(user_type=c.EXTENSION)

    def list(self, request, *args, **kwargs):
        officers = User.objects.filter(user_type=c.EXTENSION)
        serializer = self.serializer_class(officers, many=True)

        return Response(
            {'data': serializer.data},
            status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        officer = self.get_object()
        serializer = self.serializer_class(officer)

        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], permission_classes=[AllowAny], detail=True)
    def create_profile(self, request, pk=None):
        officer = self.get_object()
        role = request.data.get('role', None)
        description = request.data.get('description', None)

        profile = ExtensionProfile.objects.create(
            role=role,
            description=description,
            user=officer
        )

        serializer = ExtensionProfileSerializer(profile)

        return Response(
            {
                'data': serializer.data
            },
            status.HTTP_201_CREATED
        )
