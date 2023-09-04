from rest_framework import serializers
from users.models import User
from customers.models import Customer

class LiteCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("birthdate","timezone")


class UserSerializer(serializers.ModelSerializer):
    customer = LiteCustomerSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id","username","first_name","last_name","date_joined","email","customer")
        write_only_fields=("password")
        read_only_fields=("date_joined","is_active")

