from rest_framework.views import APIView
from .models import Teacher, Student, Group
from django.http import JsonResponse
from profiles.serializers import TeacherSerializer, StudentSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated


class GroupList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        data = request.data
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class UserList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        profiles = User.objects.all()
        serializer = UserSerializer(profiles, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)


class TeacherList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        profiles = Teacher.objects.all()
        serializer = TeacherSerializer(profiles, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        data = request.data
        serializer = TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class StudentList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = {"detail": "You are not authorize"}
        profiles = Student.objects.all()
        serializer = StudentSerializer(profiles, many=True)
        if request.user.is_authenticated:
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(data, safe=False)

    def post(self, request, format=None):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TeacherDetail(APIView):
    def get(self, request, user_id, format=None):
        profile_one = Teacher.objects.get(user_id=user_id)
        serializer = TeacherSerializer(profile_one)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            data = request.data
            profile_one = Teacher.objects.get(user_id=user_id)
            serializer = TeacherSerializer(profile_one, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"PUT": False, "ERROR": "try to change another user"}, status=400)

    def patch(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            data = request.data
            profile_one = Teacher.objects.get(user_id=user_id)
            serializer = TeacherSerializer(profile_one, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"PTCH": False, "ERROR": "try to change another user"}, status=400)

    def delete(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            user_one = User.objects.get(id=user_id)
            user_one.delete()
            data = {
                "user": "deleted"
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({"DEL": False, "ERROR": "try to change another user"}, status=400)


class StudentDetail(APIView):
    def get(self, request, user_id, format=None):
        profile_one = Student.objects.get(user_id=user_id)
        serializer = StudentSerializer(profile_one)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            data = request.data
            profile_one = Student.objects.get(user_id=user_id)
            serializer = StudentSerializer(profile_one, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"PUT": False, "ERROR": "try to change another user"}, status=400)

    def patch(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            data = request.data
            profile_one = Student.objects.get(user_id=user_id)
            serializer = StudentSerializer(profile_one, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({"PTCH": False, "ERROR": "try to change another user"}, status=400)

    def delete(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            user_one = User.objects.get(id=user_id)
            user_one.delete()
            data = {
                "user": "deleted"
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({"DEL": False, "ERROR": "try to change another user"}, status=400)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            user = User.objects.get(username=data['username'])
            response = UserSerializer(user).data
            user_id = response['id']
            if Teacher.objects.filter(user_id=user_id):
                response['employee'] = 'teacher'
            elif Student.objects.filter(user_id=user_id):
                response['employee'] = 'student'
            return JsonResponse(response)
        else:
            return JsonResponse({"login": False})


class UnAuth(ObtainAuthToken):
    def post(self, request, format=None):
        logout(request)
        return JsonResponse({"logout": True})
