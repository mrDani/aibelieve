from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from user.serializers import RegistrationSerializer,ChangePasswordSerializer,VerificationCodeSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import send_code_to_user,verify_otp


from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['first_name'] = user.first_name
        token['email'] = user.email
        # ...

        return token
    
# validate method is overridden to add extra responses to the data returned by the parent class's validate method.
    def validate(self, attrs):
        # call validates the provided attributes using the parent class's validate method and returns the validated data.
        data = super().validate(attrs)

        # Add extra responses
        # Adds the user id to the response
        data.update({'user_id': self.user.id})

        # Finally, the updated data dictionary is returned.
        return data
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer 


@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # Save the user
            send_code_to_user(user.email)  # Send email to the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    if request.method == 'PUT':
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def code_verification(request):
    serializer = VerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        user_email = request.user.email

        if verify_otp(user_email, code):
            return Response({'message': 'Code is valid', 'is_verified': True})
        else:
            return Response({'message': 'Invalid code or expired'}, status=400)
    else:
        return Response(serializer.errors, status=400)




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def resend_verification_code(request):
#     try:
#         otp_instance = OneTimePassword.objects.get(user=request.user)
#         # If an instance already exists, update the code and return
#         new_code = generate_otp()
#         otp_instance.code = new_code
#         otp_instance.save()
#     except OneTimePassword.DoesNotExist:
#         # If no instance exists, create a new one
#         new_code = generate_otp()
#         otp_instance = OneTimePassword.objects.create(user=request.user, code=new_code)

#     # Send email with new code
#     if send_code_to_user(request.user.email, new_code):
#         return Response({'message': 'New verification code sent successfully'})
#     else:
#         return Response({'message': 'Error sending new verification code'}, status=500)





