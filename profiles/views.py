from rest_framework.views import APIView
from .models import Profile
from django.http import JsonResponse
from profiles.serializers import ProfileSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class ProfileList(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class ProfileDetail(APIView):
    def get(self, request, user_id, format=None):
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, user_id, format=None):
        data = JSONParser().parse(request)
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request, user_id, format=None):
        data = JSONParser().parse(request)
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, user_id, format=None):
        user_one = User.objects.get(id=user_id)
        user_one.delete()
        data = {
            "user": "deleted"
        }
        return JsonResponse(data, safe=False)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, format=None):
        err={
                'error': 'username or password is incorrect'
            }
        data = JSONParser().parse(request)
        user = User.objects.filter(username=data['username'])
        if user:
            user = User.objects.get(username=data['username'])
            if user.check_password(data['password']):
                token = Token.objects.get(user=user)
                return JsonResponse({
                    'token': token.key
                },status=200)
            else:
                return Response(err)
        else:
            return Response(err)