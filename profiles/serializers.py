from rest_framework import serializers
from profiles.models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)

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
        is_dict = {}
        for key in validated_data.keys():
            is_dict[key] = 1

        if is_dict.get('username'):
            if instance.username == validated_data['username']:
                if is_dict.get('email'):
                    if instance.email != validated_data['email']:
                        valid_email = User.objects.filter(email=validated_data['email'])
                        if valid_email:
                            raise serializers.ValidationError("User with this email already exist")
            else:
                valid_username = User.objects.filter(username=validated_data['username'])
                if valid_username:
                    raise serializers.ValidationError("This user already exist")
        else:
            if is_dict.get('email'):
                if instance.email != validated_data['email']:
                    valid_email = User.objects.filter(email=validated_data['email'])
                    if valid_email:
                        raise serializers.ValidationError("User with this email already exist")

        if is_dict.get('username'):
            instance.username = (validated_data['username'])
        if is_dict.get('email'):
            instance.email = (validated_data['email'])
        if is_dict.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Profile
        fields = ('user', 'good', 'employee')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile_one = Profile.objects.create(user=user)
        for (key, value) in validated_data.items():
            setattr(profile_one, key, value)
        profile_one.save()
        return profile_one

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            if key=='user':
                instance.user = UserSerializer.update(UserSerializer(), instance.user, validated_data=value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance
