from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from django.contrib.auth.models import User

from account.serializers import UserRegistrationSerializer, UserLoginSerializer



# Generate Token Manually
def get_token_for_users(user):
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    except Exception as e:
        # Log the error for investigation
        print(f"Token generation failed for user {user.email}: {e}")
        # Return None or an empty dictionary indicating failure
        return None


# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    """
        View to register a new user in the system.
        The view will receive two parameters (username and password).
        If both are valid it returns a success message with a token that can be used on header Authorization to make authenticated requests.
        It should create a new user with that username and hashed password, then generate a JWT token for authentication.
        If both are valid, it will create a new user with that username and password,
        then generate a JWT token for authentication.
        Otherwise, it returns errors about what went wrong.
    """
    def post(self, request, format=None):
        serializer =  UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Generate Token
            token = get_token_for_users(user)
            return Response({'token': token, 'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Get the user object based on the provided email and password
            user = authenticate(email=email, password=password)
            if user is not None:
                # Generate a token for the authenticated user
                token =  get_token_for_users(user)
                # Return a success response with the token
                return Response({
                    'token':token,
                    "msg":"Login Success",
                    'usertype':serializer.validated_data['usertype']
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

        

