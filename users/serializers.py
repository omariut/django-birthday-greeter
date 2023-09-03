from rest_framework import serializers
from users.models import User
from customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ("password",)

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'