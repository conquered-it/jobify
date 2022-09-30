from email.mime import application
from urllib import response
from xml.dom import ValidationErr
from django.conf import settings
from jobportal.models import Skill, Applicant, Domain, Application
from django.http import JsonResponse, FileResponse, HttpResponse
from jobportal.api.serializers import SkillSerializer, ApplicantSignupSerializer, ApplicantGetSerializer, ApplicantUpdateSerializer, ApplicantListSerializer, DomainGetSerializer, DomainCreateSerializer, DomainUpdateSerializer, ApplicationSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer, ApplicantApplicationSerializer, DomainApplicationSerializer
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django.views.generic.detail import BaseDetailView
from rest_framework.response import Response
from jobportal.api.pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jobportal.api.permissions import IsAdminUserOrApplicant, IsApplicant, IsAdminUserOrReadOnly, IsAdminUserOrApplicantReadOnly
from rest_framework.exceptions import ValidationError


class ApplicantSignup(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSignupSerializer


class ApplicantList(generics.ListAPIView):
    queryset = Applicant.objects.all().order_by('id')
    serializer_class = ApplicantListSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name',
                     'last_name', 'email', 'phone_number', 'skills__name']
    permission_classes = [IsAdminUser]


class ApplicantGet(generics.RetrieveDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantGetSerializer
    permission_classes = [IsAdminUserOrApplicant]


class ApplicantUpdate(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantUpdateSerializer
    permission_classes = [IsApplicant]


class ApplicantResume(BaseDetailView):

    def get(self, request, pk):
        if not (request.user and (request.user.is_staff or request.user.id == pk)):
            return JsonResponse({"detail": "You do not have permission to perform this action."}, status=404)
        applicant = Applicant.objects.get(pk=pk)
        resume = applicant.resume
        try:
            response = HttpResponse(
                resume.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename={}Resume.pdf'.format(
                Applicant.first_name)
            return response
        except:
            return JsonResponse({"Error": 'Resume not found'}, status=404)


class ApplicantImage(BaseDetailView):

    def get(self, request, pk):
        if not (request.user and (request.user.is_staff or request.user.id == pk)):
            return JsonResponse({"detail": "You do not have permission to perform this action."}, status=404)
        applicant = Applicant.objects.get(pk=pk)
        image = applicant.image
        try:
            response = HttpResponse(
                image.read(), content_type='application/jpg')
            response['Content-Disposition'] = 'filename={}Image.jpg'.format(
                Applicant.first_name)
            return response
        except:
            return JsonResponse({"Error": 'Image not found'}, status=404)


class ApplicantApplication(generics.ListAPIView):
    queryset = Application.objects.all().order_by('id')
    serializer_class = ApplicantApplicationSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [IsAdminUserOrApplicant]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.kwargs['pk'])


class DomainCreate(generics.CreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainCreateSerializer
    permission_classes = [IsAdminUser]


class DomainList(generics.ListAPIView):
    queryset = Domain.objects.all().order_by('id')
    serializer_class = DomainGetSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'skills_required__name']


class DomainGet(generics.RetrieveDestroyAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainGetSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class DomainUpdate(generics.UpdateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainUpdateSerializer
    permission_classes = [IsAdminUser]


class DomainApplication(generics.ListAPIView):
    queryset = Application.objects.all().order_by('id')
    serializer_class = DomainApplicationSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Application.objects.filter(domain=self.kwargs['pk'])


class ApplicationCreate(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Application.objects.filter(applicant=self.request.user, status='UNREVIEWED').exists():
            raise ValidationError("You've already applied for this domain")
        serializer.save(applicant=self.request.user, status='UNREVIEWED')


class ApplicationList(generics.ListAPIView):
    queryset = Application.objects.all().order_by('id')
    serializer_class = ApplicationSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'domain__name']
    permission_classes = [IsAdminUser]


class ApplicationDetail(generics.RetrieveDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUserOrApplicantReadOnly]


class ApplicationUpdate(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [IsAdminUser]


class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAdminUserOrReadOnly]


class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUserOrReadOnly]
