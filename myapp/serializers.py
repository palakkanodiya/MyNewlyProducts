from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product
# from django.contrib.auth.models import AbstractUser

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id' , 'username' , 'email','role']


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], required=False)
    class Meta:
        model = User
        fields = ['username' , 'email', 'password','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.get('role', 'buyer')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # role=validated_data['role'],
            role=role
        )
        # role = validated_data.get('role','buyer')
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only = True)

##############new
class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username' , read_only=True)
    class Meta:
        model = Product
        fields = ['id','name', 'description','price','seller_name','created_at']
        read_only_field = ['seller_name','created_at']
    
