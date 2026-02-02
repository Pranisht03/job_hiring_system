from rest_framework import serializers
from accounts.models import CustomUser
from accounts.models import JobSeekerProfile
from jobs.models import Job

class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
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
    class Meta:
        model = CustomUser
        fields = ['company_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
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

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(required=False)
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source='company.username', read_only=True
    )

    class Meta:
        model = Job
        fields = [
            'id',
            'company_name',
            'job_title',
            'job_description',
            'skills_required',
            'experience_required',
            'salary',
            'job_type',
            'location',
            'vacancies',
            'last_date_to_apply',
            'created_at',
        ]
