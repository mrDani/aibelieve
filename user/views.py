from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from user.serializers import RegistrationSerializer,ChangePasswordSerializer,VerificationCodeSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import send_code_to_user,verify_otp
from django.http import JsonResponse
from .models import OneTimePassword

import requests


from .models import OneTimePassword
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
<<<<<<< HEAD
        token['last_name'] = user.last_name
=======
        token['last_name'] = user.first_name
>>>>>>> a7d983ff760f3645686ea062f7c5a21b144bfc45
        token['email'] = user.email
        # ...

        return token
    


    def validate(self, attrs):
        # Call validates the provided attributes using the parent class's validate method and returns the validated data.
        data = super().validate(attrs)

        # Add extra responses
        # Adds the user id to the response
        data.update({'user_id': self.user.id})
        full_name = f"{self.user.first_name} {self.user.last_name}"
        data.update({'full_name': full_name})
        

        # Add full name to the response
        full_name = f"{self.user.first_name} {self.user.last_name}"
        data.update({'full_name': full_name})

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
def code_verification(request):
    if request.method == 'POST':
        otp_code = request.data.get('code') # Extract the OTP code from the request data
        if not otp_code:
            # If OTP code is not provided, return a bad request response
            return Response({'message': 'Passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to find a OneTimePassword object with the provided OTP code
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True  # If the user is not verified, mark them as verified and save
                user.save()
                return Response({'message': 'Account email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Code is invalid, user already verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Invalid passcode'}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
<<<<<<< HEAD
def code_verification(request):
    if request.method == 'POST':
        otp_code = request.data.get('code') # Extract the OTP code from the request data
        if not otp_code:
            return Response({'message': 'Passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)# Try to find a OneTimePassword object with the provided OTP code
            user = user_code_obj.user

            if not user.is_verified:
                # If the user is not verified, mark them as verified and save
                user.is_verified = True
                user.save()
                return Response({'message': 'Account email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Code is invalid, user already verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Invalid passcode'}, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

=======
def resend_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

>>>>>>> a7d983ff760f3645686ea062f7c5a21b144bfc45
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    send_result = send_code_to_user(user.email)
    if "Failed" in send_result:
        return Response({'error': send_result}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
<<<<<<< HEAD


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
=======
    
    # Assuming the send_code_to_user function returns a success message on success
    if send_result == "OTP sent successfully":
        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    else:
        # Handling any other unexpected response from the utility function
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
>>>>>>> a7d983ff760f3645686ea062f7c5a21b144bfc45







# Create your views here.

@api_view(['GET'])
def jokeView(request):
    url = "https://world-of-jokes1.p.rapidapi.com/v1/jokes/joke-of-the-day"

    headers = {
        "X-RapidAPI-Key": "875e36e896msh9e84973856854aap18d4e5jsnc10cd914eabe",
        "X-RapidAPI-Host": "world-of-jokes1.p.rapidapi.com"
    }


    
    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
    return JsonResponse(data)




@api_view(['GET'])
def motivationView(request):
    url = "https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote"

    querystring = {"token":"ipworld.info"}

    headers = {
        "X-RapidAPI-Key": "875e36e896msh9e84973856854aap18d4e5jsnc10cd914eabe",
        "X-RapidAPI-Host": "quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json()) 
    if response.status_code == 200:
        data = response.json()
    return JsonResponse(data)
 
            