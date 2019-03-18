from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from .models import Teacher, Student, Group, StudentGroup
from django.http import JsonResponse
from profiles.serializers import TeacherSerializer, StudentSerializer, UserSerializer, GroupSerializer, \
    StudentGroupSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404


class SelfUpdate(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.filter(id=view.kwargs['pk'])
        if not user:
            return False
        user = User.objects.get(id=view.kwargs['pk'])
        if request.user == user:
            return True
        return False


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        student = Student.objects.filter(user_id=request.user.id)
        if student:
            return True
        return False


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        teacher = Teacher.objects.filter(user_id=request.user.id)
        if teacher:
            return True
        return False


class IsTeacherAdminOrStudentUpdate(BasePermission):
    def has_permission(self, request, view):
        if User.objects.get(id=request.user.id).is_superuser:
            return True
        student = Student.objects.filter(user_id=request.user.id)
        if student:
            student = Student.objects.get(user_id=request.user.id)
            if student.user_id == request.data['student']:
                return True
        teacher = Teacher.objects.filter(user_id=request.user.id)
        if teacher:
            teacher = Teacher.objects.get(user_id=request.user.id)
            if teacher.is_admin:
                return True
        return False


class ReadCreate(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    pass


class Students(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_permissions(self):

        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve' or not self.action:
            permission_classes = [AllowAny]
        else:
            permission_classes = [SelfUpdate]

        return [permission() for permission in permission_classes]


class Teachers(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [SelfUpdate]

        return [permission() for permission in permission_classes]


class Users(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve' or not self.action:
            permission_classes = [AllowAny]
        else:
            permission_classes = [SelfUpdate]

        return [permission() for permission in permission_classes]


class Groups(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class StudentsGroups(ReadCreate):
    serializer_class = StudentGroupSerializer
    queryset = StudentGroup.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsTeacherAdminOrStudentUpdate]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class GroupsFromStudent(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = StudentGroup.objects.filter(student_id=pk)
        serializer = StudentGroupSerializer(queryset, many=True)
        return Response(serializer.data)

class StudentsFromGroup(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = StudentGroup.objects.filter(group_id=pk)
        serializer = StudentGroupSerializer(queryset, many=True)
        return Response(serializer.data)

class Auth(ObtainAuthToken):
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
            return JsonResponse({"login": False}, status=200)


class UnAuth(ObtainAuthToken):
    def post(self, request, format=None):
        logout(request)
        return JsonResponse({"logout": True})
