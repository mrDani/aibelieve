from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields=('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only':True}}

    # Validate the password confirmation
    def validate(self, attrs):
        password = attrs.get('password')
        password2 =attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match")
        return attrs
    
   
   # Create method to handle user creation
    def create(self, validated_data):
        validated_data.pop('password2', None)

        # Extract the password from validated_data
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        # Use Django's set_password method to hash and set the password
        user.set_password(password)
        # Save the user object with the hashed password
        user.save()
        return user



class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True, max_length=20, style={'input_type': 'password'}, write_only=True)
    new_password=serializers.CharField(required=True, max_length=20, style={'input_type': 'password'}, write_only=True)
    confirm_password=serializers.CharField(required=True, max_length=20, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        user=self.context.get('user')

        # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            raise serializers.ValidationError('old password is incorrect!')
        
        if new_password != confirm_password:
            raise serializers.ValidationError("New Password and Confirm Password don't match")
        
        # Set the new password and hash it before saving
        user.set_password(new_password)
        user.save()
        return attrs
    


# Serializer for resetting user password via email
class resetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True, max_length=50, style={'input_type':'email'}, write_only=True)