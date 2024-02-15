from rest_framework  import serializers
from django.contrib.auth.hashers import make_password
from account.models import User
from rest_framework.authentication import authenticate


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     # We are writing this because we need confirm password feild in our registration Request
#     password2 = serializers.CharField(write_only=True)
#     userType = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email','password', 'password2', 'userType']
#         extra_kwargs = {
#             'password':{'write_only':True}
#         }
    
#     # Validating Password and Confirm Password while Registration
#     def validate(self, attrs):            # attr = data
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         if password != password2:
#             raise serializers.ValidationError("Password And Confirm Password does not match")
#         return attrs
    
#     def create(self, validated_data):    # Called when creating a new instance using Model
#         userType = validated_data.pop( "userType")
#         # is_employer = userType.lower() == 'employer'
#         # is_jobseeker  = userType.lower() == 'jobseeker'
#         is_employer = user == 'employer'
#         is_jobseeker = user == 'jobseeker'
#         # Hash the password before saving
#         validated_data['password'] = make_password(validated_data['password'])
#         user = User.objects.create_user(**validated_data)

#         if is_employer:
#             user.is_employer = True
#         elif is_jobseeker:
#             user.is_jobseeker = True
#         user.save()
#         return user
class UserRegistrationSerializer(serializers.ModelField):
    """
        A custom field for handling the registration of both employers and job seekers.
    """
    # We are writing this because we need confirm password feild in our registration Request
    password2  = serializers.CharField(write_only=True)
    userType = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'userType')
        extra_kwargs  = {'password': {'write_only': True}}
        # Validating  Password and Confirm Password while Registration
        def validate(self, attrs):
            password = attrs.get('password')            
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError("Password And Confirm Password does not match")
            return attrs
        
        def create(self, validated_data):      # Called when creating a new instance using Model
            userType = validated_data.pop('userType')
            # Hash password  before saving
            validated_data['password'] = make_password(validated_data['password'])
            user = User.objects.create_user(**validated_data)

            if userType == 'employer':
                user.is_employer = True
            elif userType == 'jobseeker':
                user.is_jobseeker = True
            user.save()
            return user



