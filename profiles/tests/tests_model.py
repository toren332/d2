from django.test import TestCase
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
import traceback



class ProfileModelTest(TestCase):

    def test_creating_simple_profile(self):
        data =  \
            {
                "user":
                {
                    "username": "ttt",
                    "email": "ttt@ttt.ttt",
                    "password": "mypassword"
                }
            }
        profile = ProfileSerializer.create(ProfileSerializer(), validated_data=data)
        profile2 = Profile.objects.get(id=1)
        self.assertEquals(profile2, profile)

    def test_creating_two_identic_profiles(self):
        data =  \
            {
                "user":
                {
                    "username": "ttt",
                    "email": "ttt@ttt.ttt",
                    "password": "mypassword"
                }
            }
        data2 = \
            {
                "user":
                    {
                        "username": "ttt",
                        "email": "ttt@ttt.ttt",
                        "password": "mypassword"
                    }
            }
        error = False
        profile1 = ProfileSerializer.create(ProfileSerializer(), validated_data=data)
        try:
            profile2 = ProfileSerializer.create(ProfileSerializer(), validated_data=data2)
        except:
            error = 'This user already exist' in traceback.format_exc()
            self.assertTrue(True)
        self.assertTrue(error)

    def test_creating_two_profiles_with_identic_usernames(self):
        data = \
            {
                "user":
                    {
                        "username": "ttt",
                        "email": "ttt@ttt.ttt1",
                        "password": "mypassword"
                    }
            }
        data2 = \
            {
                "user":
                    {
                        "username": "ttt",
                        "email": "ttt@ttt.ttt2",
                        "password": "mypassword"
                    }
            }
        error = False
        profile1 = ProfileSerializer.create(ProfileSerializer(), validated_data=data)
        try:
            profile2 = ProfileSerializer.create(ProfileSerializer(), validated_data=data2)
        except:
            error = 'This user already exist' in traceback.format_exc()
            self.assertTrue(True)
        self.assertTrue(error)

    def test_creating_two_profiles_with_identic_emails(self):
        data = \
            {
                "user":
                    {
                        "username": "ttt1",
                        "email": "ttt@ttt.ttt",
                        "password": "mypassword"
                    }
            }
        data2 = \
            {
                "user":
                    {
                        "username": "ttt2",
                        "email": "ttt@ttt.ttt",
                        "password": "mypassword"
                    }
            }
        error = False
        profile1 = ProfileSerializer.create(ProfileSerializer(), validated_data=data)
        try:
            profile2 = ProfileSerializer.create(ProfileSerializer(), validated_data=data2)
        except:
            error = 'User with this email already exist' in traceback.format_exc()
            self.assertTrue(True)
        self.assertTrue(error)