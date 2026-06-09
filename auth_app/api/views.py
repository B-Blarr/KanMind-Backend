from rest_framework import generics
from auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer, \
    LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname' : saved_account.first_name,
                'email' : saved_account.email,
                'user_id': saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'fullname' : user.first_name,
                'email' : user.email,
                'user_id': user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'email not found'},
                            status=status.HTTP_404_NOT_FOUND)
        data = {
            'id': user.id,
            'email': user.email,
            'fullname': user.first_name
        }
        return Response(data, status=status.HTTP_200_OK)