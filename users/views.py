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
from users.serializers import UserSerializer, UserTokenSerializer
from users.utils import delete_cache, get_cache, set_cache
from users.helpers import create_tokens
from django.db import transaction
from customers.models import Customer
from django.core.exceptions import BadRequest

logger = logging.getLogger('django')
User=get_user_model()
class UnprocessableEntity(APIException):
    status_code = 406
    default_code = 406
    default_detail = 'unprocessable entity'

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request: Request) -> Response:
    email = request.data.get('email')
    try:
        User.objects.get(email=email)
        raise UnprocessableEntity(
            detail='user with this email already exists', code=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        user = User()
        user.username = request.data.get('username')
        user.email=email
        user.set_password(raw_password=request.data.get('password'))
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user_type=request.data.get("user_type")

        if user_type:
            user.user_type=user_type
        
        if User.objects.filter(username = user.username).exists():
            raise UnprocessableEntity(
                detail='username already exists', code=status.HTTP_406_NOT_ACCEPTABLE)
        
        with transaction.atomic():
            user.save() # save user

            # create customer is user_type is customer

            if user.user_type=='customer':
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
                
        return Response(data={'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        raise ValidationError(
            detail='username and password is required', code=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username__exact=username)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='invalid password',
                                  code=status.HTTP_400_BAD_REQUEST)
        access_token, refresh_token = create_tokens(user=user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user':UserSerializer(instance=user).data
        }
        set_cache(key=f'{username}_token_data', value=json.dumps(UserTokenSerializer(user).data), ttl=5*60*60)
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)



