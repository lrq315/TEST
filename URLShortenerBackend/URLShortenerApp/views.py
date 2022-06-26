from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny

import jwt, datetime

from .serializers import UserSerializers, URLShortenerResultSerializers
from .models import User, URLShortenerResult

from .authentication import TokenAuthentication
from .services import URLShortenerService


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id = payload['id']).first()

        serializer = UserSerializers(user)

        return Response(serializer.data)


class URLShortenerView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        serializer = URLShortenerResultSerializers(data=request.data)
        if not serializer.is_valid():
            return Response({'errors':serializer.errors}, status.HTTP_400_BAD_REQUEST)
        long_url = serializer.validated_data['long_url']
        urlshortener_service = URLShortenerService(long_url)
        short_url = urlshortener_service.generate_short_url()
        if short_url:
            urlshortenerresult = URLShortenerResult(user = self.get_user(request), long_url=long_url, short_url=short_url)
            urlshortenerresult.save()
            return Response({"short_url":short_url}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": "Sever wrong!"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        user = self.get_user(request)
        serializer = URLShortenerResultSerializers(URLShortenerResult.objects.filter(user = user), many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_user(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return User.objects.filter(id = payload['id']).first()