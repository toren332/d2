from rest_framework.views import APIView
from .models import Teacher, Student, Group, StudentGroup
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


class StudentSetGroup(APIView):
    def post(self, request, user_id, format=None):
        current_user = request.user
        if current_user.id == user_id:
            student = Student.objects.get(user_id=user_id)
            data = request.data
            if data.get('group_ids'):
                group_ids = data['group_ids']
                for group_id in group_ids:
                    valid_group = Group.objects.filter(id=group_id)
                    if not valid_group:
                        return JsonResponse(
                            {"StudentSetGroup": False, "ERROR": "one or more group ids is invalid"},
                            status=400)
                    else:
                        if Group.objects.get(id=group_id).is_primary:
                            return JsonResponse({"StudentSetGroup": False, "ERROR": "try to set primary user group"},
                                                status=403)
                for group_id in group_ids:
                    group = Group.objects.get(id=group_id)
                    StudentGroup.objects.update_or_create(group=group, student=student)
            else:
                return JsonResponse({"StudentSetGroup": False, "ERROR": "request error, wait for group_ids field of "
                                                                        "list"}, status=400)
        else:
            return JsonResponse({"StudentSetGroup": False, "ERROR": "try to set another user in group"},
                                status=403)
        return JsonResponse({"StudentSetGroup": True}, status=201)

    def get(self, request, user_id, format=None):
        valid_student = Student.objects.filter(user_id=user_id)
        if valid_student:
            student = Student.objects.get(user_id=user_id)
            groups0 = StudentGroup.objects.filter(student=student)
            groups=[]
            for i in groups0:
                groups.append(i.group)
            serializer = GroupSerializer(groups, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({"StudentGetGroup": False, "ERROR": "student id is invalid"}, status=400)


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
