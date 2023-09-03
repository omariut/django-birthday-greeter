from customers.models import Customer
from rest_framework import serializers
from users.models import User

class LiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email","first_name","last_name")


class CustomerSerializer(serializers.ModelSerializer):
    user = LiteUserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = "__all__"