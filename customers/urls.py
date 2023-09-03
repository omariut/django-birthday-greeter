
from django.urls import path
from customers.views import CustomerListAPIView,CustomerRetrieveUpdateDestroyAPIView
urlpatterns = [
    path("customers", CustomerListAPIView.as_view(),name='customer-list'),
    path("customers/<int:user_id>", CustomerRetrieveUpdateDestroyAPIView.as_view(),name='customer-single-view-update-delete'),

]