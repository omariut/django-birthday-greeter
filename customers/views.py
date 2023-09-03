from rest_framework import generics
from customers.models import Customer
from customers.serializers import CustomerSerializer
from users.permissions import IsAdmin,IsCustomer,IsObjectOwner

class CustomerListAPIView(generics.ListAPIView):
    queryset = Customer.objects.filter().select_related('user')
    serializer_class = CustomerSerializer
    permission_classes=(IsAdmin,)


class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.filter().select_related('user')
    serializer_class = CustomerSerializer
    permission_classes=(IsAdmin|IsObjectOwner,)
    lookup_field='user_id'


