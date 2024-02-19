from rest_framework  import serializers
from django.contrib.auth.hashers import make_password
from account.models import User
from rest_framework.authentication import authenticate
from django.contrib.auth.password_validation import validate_password





class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    usertype = serializers.ChoiceField(choices=[('employer', 'Employer'), ('jobseeker', 'Job Seeker')], default='jobseeker')

    class Meta:
        model = User
        fields = ('username', 'email','password', 'password2','usertype')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password And Confirm Password does not match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        usertype = validated_data.get('usertype')
        if usertype == 'employer':
            user.is_employer = True
        elif usertype == 'jobseeker':
            user.is_jobseeker = True
        user.save()
        return user




class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # Check id the user exists and the password is correct
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        # Check if the user is an employer or a jobseeker
        if user.is_employer:
            usertype = 'employer'
        elif user.is_jobseeker:
            usertype = 'jobseeker'
        else:
            raise serializers.ValidationError("User account is not activated")
        # Set the user type in the serialized data
        attrs['usertype'] = usertype
        return attrs



        


