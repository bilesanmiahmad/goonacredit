from rest_framework import serializers

from django.contrib.auth import authenticate

from accounts.models import FarmerProfile, User, MerchantProfile, ExtensionProfile


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField(source='date_joined_str')
    last_login = serializers.ReadOnlyField(source='last_login_str')

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'country_code', 'phone_number', 'gender',
            'date_of_birth', 'auth_token', 'user_type', 'last_login',
            'date_joined'
                  ]


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email__iexact=value)
            if user:
                raise serializers.ValidationError(
                    "The email already exists"
                )
        except User.DoesNotExist:
            pass

        return value

    def validate_phone(self, value):
        try:
            user = User.objects.get(phone_number__iexact=value)
            if user:
                raise serializers.ValidationError(
                    "The phone number already exists."
                )
        except User.DoesNotExist:
            pass

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone']
        )

        return user


class SignInSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        user = authenticate(phone_number=phone, password=password)

        if user:
            data['user'] = user

            return data

        raise serializers.ValidationError("User Not Found")


class MerchantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MerchantProfile
        fields = ['id', 'user', 'product', 'description', 'created_at', 'updated_at']


class ExtensionProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ExtensionProfile
        fields = ['id', 'user', 'role', 'description', 'created_at', 'updated_at']


class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'user', 'address', 'family_size',
            'farm_location', 'farm_size',
            'credit_rating', 'photo'
        ]

