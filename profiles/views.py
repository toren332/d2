from rest_framework.views import APIView
from .models import Profile
from django.http import JsonResponse
from profiles.serializers import ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated


class ProfileList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        data = request.data
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
        data = request.data
        profile_one = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(profile_one, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request, user_id, format=None):
        data = request.data
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
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({"login": True})
        else:
            return JsonResponse({"login": False})


class UnAuth(ObtainAuthToken):
    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            logout(request)
            return JsonResponse({"login": "unlogged"})
        else:
            return JsonResponse({"login": "unlogging error"})
