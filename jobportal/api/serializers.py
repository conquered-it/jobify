from unittest import mock
from rest_framework import serializers
from jobportal.models import Skill, Applicant, Domain, Application


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name',)


class ApplicantSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        applicant = Applicant(**validated_data)
        applicant.set_password(password)
        applicant.save()
        return applicant


class ApplicantGetSerializer(serializers.HyperlinkedModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    resume = serializers.HyperlinkedIdentityField(
        view_name='jobportal:applicant-resume')
    image = serializers.HyperlinkedIdentityField(
        view_name='jobportal:applicant-image')

    class Meta:
        model = Applicant
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'image', 'resume', 'linkedin_url',
                  'skills', 'description', 'achievements', 'experience', 'education', 'country', 'state', 'city')


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'image', 'resume', 'linkedin_url',
                  'skills', 'description', 'achievements', 'experience', 'education', 'country', 'state', 'city')


class ApplicantListSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="jobportal:applicant-get")
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Applicant
        fields = ('url', 'name', 'image', 'skills',
                  'country', 'state', 'city', 'email')

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


class DomainGetSerializer(serializers.ModelSerializer):
    skills_required = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = '__all__'


class DomainCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class DomainUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class DomainItemSerializer(serializers.ModelSerializer):
    skills_required = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = ('name', 'skills_required',)


class DomainApplicationSerializer(serializers.HyperlinkedModelSerializer):
    applicant = serializers.HyperlinkedIdentityField(
        view_name="jobportal:applicant-get")

    class Meta:
        model = Application
        fields = ('applicant', 'status')


class ApplicantItemSerializer(serializers.HyperlinkedModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name="jobportal:applicant-get")

    class Meta:
        model = Applicant
        fields = ('profile_url',)


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantItemSerializer()
    domain = DomainItemSerializer()

    class Meta:
        model = Application
        fields = ('applicant', 'domain', 'status')


class ApplicationGetSerializer(serializers.ModelSerializer):
    applicant = ApplicantItemSerializer()
    domain = DomainItemSerializer()

    class Meta:
        model = Application
        fields = ('applicant', 'domain', 'status')


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('status',)


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('domain', )


class ApplicantApplicationSerializer(serializers.ModelSerializer):
    domain = DomainItemSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ('domain', 'status')
