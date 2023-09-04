import json
import logging
import random
import jwt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from users.serializers import UserSerializer
from users.utils import delete_cache, get_cache, set_cache
from users.helpers import create_tokens
from django.db import transaction
from customers.models import Customer
from django.core.exceptions import BadRequest
from rest_framework import generics
from users.permissions import IsAdmin
from rest_framework.permissions import AllowAny

logger = logging.getLogger('django')
User=get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    queryset=User.objects.filter().prefetch_related('customer')
    serializer_class=UserSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):

        user_type_in_payload = self.request.data.get('user_type')
        
        if user_type_in_payload:
            self.permission_classes=(IsAdmin,)
        return super().get_permissions()

    def save_customer(self,user):
        request=self.request
        birthdate=request.data.get("birthdate")
        timezone =request.data.get("timezone")

        if not birthdate:
            raise BadRequest("Birthdate Required for Customer")
        
        if not timezone:
            raise BadRequest("Timezone Required for Customer")

        Customer.objects.create(
            user=user,
            birthdate=birthdate,
            timezone=timezone
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()
            user.set_password(raw_password=self.request.data.get('password'))
            user.save()
            if user.user_type=='customer':
                self.save_customer(user)


class UserListAPIView(generics.ListAPIView):
    queryset=User.objects.filter().prefetch_related('customer')
    serializer_class=UserSerializer
    permission_classes = (IsAdmin,)