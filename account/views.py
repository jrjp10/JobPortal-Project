from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from account.serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# class UserRegistrationView(APIView):
#     renderer_classes = [UserRenderer]

#     def post(self, request, format= None):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()

#             # Use Validate data to set user types
#             is_employer = serializer.validated_data.get('is_employer')
#             is_jobseeker = serializer.validated_data.get('is_jobseeker')
#             if is_employer:
#                 user.is_employer = True
#             elif is_jobseeker:
#                 user.is_jobseeker = True
#             user.save()
            
#             # Generate token
#             token = get_token_for_users(user)
#             return Response({'token':token, 'msg':'Registration Success'}, status=status.HTTP_201_CREATED )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Bad Request
        
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
    

class UserRegistrationView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

    """
        View to register a new user in the system.
        The view will receive two parameters (username and password).
        If both are valid it returns a success message with a token that can be used on header Authorization to make authenticated requests.
        It should create a new user with that username and hashed password, then generate a JWT token for authentication.
        If both are valid, it will create a new user with that username and password,
        then generate a JWT token for authentication.
        Otherwise, it returns errors about what went wrong.
    """
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            # Use Validate data to set user types
            is_employer = serializer.validated_data.get('is_employer')
            is_jobseeker = serializer.validated_data.get('is_jobseeker')
            if is_employer:
                user.is_employer = True
            elif is_jobseeker:
                user.is_jobseeker = True
            user.save()

            # Generate tokens 
            token = get_token_for_users(user)
            return Response({'token': token, 'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

        

