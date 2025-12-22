from rest_framework import serializers
from accounts.models import CustomUser

class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match!"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser(
            email=validated_data['email'],
            full_name=validated_data.get('full_name', ''),
            username=validated_data['email'],
            is_job_seeker=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompanyRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['company_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match!"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser(
            email=validated_data['email'],
            company_name=validated_data.get('company_name', ''),
            username=validated_data['email'],
            is_company=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('jobseeker', 'Job Seeker'), ('company', 'Company')])
