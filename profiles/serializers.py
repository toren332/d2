from rest_framework import serializers
from profiles.models import Teacher, Student, Group, StudentGroup
from django.contrib.auth.models import User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', 'is_primary', 'id')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)

    def create(self, validated_data):
        valid_username = User.objects.filter(username=validated_data['username'])
        valid_email = User.objects.filter(email=validated_data['email'])
        if valid_username:
            raise serializers.ValidationError("This user already exist")
        if valid_email:
            raise serializers.ValidationError("User with this email already exist")
        else:
            user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                            validated_data['password'])
        return user

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if key == 'username':
                users_by_username = User.objects.filter(username=validated_data['username'])
                if users_by_username:
                    user_by_username = users_by_username[0]
                    if user_by_username.username != instance.username:
                        raise serializers.ValidationError("This username already used")
                    else:
                        setattr(instance, key, value)
                else:
                    setattr(instance, key, value)
            if key == 'email':
                users_by_email = User.objects.filter(email=validated_data['email'])
                if users_by_email:
                    user_by_email = users_by_email[0]
                    if user_by_email.email != instance.email:
                        raise serializers.ValidationError("This email already used")
                    else:
                        setattr(instance, key, value)
                else:
                    setattr(instance, key, value)
            if key == 'password':
                instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile_one = Teacher.objects.create(user=user)
        for (key, value) in validated_data.items():
            if key != 'is_verified' or key != 'is_admin':
                setattr(profile_one, key, value)
        profile_one.save()
        return profile_one

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if key == 'user':
                instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
            else:
                if key != 'is_verified':  # TODO: добавить проверку на администратора и разрешить ему верифицировать
                    setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = Teacher
        fields = ('user', 'first_name', 'middle_name', 'last_name', 'is_verified', 'is_admin')




class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ('user', 'first_name', 'middle_name', 'last_name')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile_one = Student.objects.create(user=user)
        for (key, value) in validated_data.items():
            setattr(profile_one, key, value)
        profile_one.save()
        return profile_one

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if key == 'user':
                instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance


class StudentGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentGroup
        fields = ('student', 'group')
