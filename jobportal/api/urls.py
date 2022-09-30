from django.urls import path
from jobportal.api.views import ApplicantSignup, ApplicantList, ApplicantGet, ApplicantUpdate, ApplicantResume, ApplicantImage, DomainList, DomainGet, DomainCreate, DomainUpdate, ApplicationList, ApplicationCreate, ApplicationDetail, ApplicationUpdate, SkillList, SkillDetail, ApplicantApplication, DomainApplication

urlpatterns = [
    path('applicant/signup/', ApplicantSignup.as_view(), name='applicant-signup'),
    path('applicant/', ApplicantList.as_view(), name='applicant-list'),
    path('applicant/<int:pk>/', ApplicantGet.as_view(),
         name='applicant-get'),
    path('applicant/<int:pk>/update/', ApplicantUpdate.as_view(),
         name='applicant-update'),
    path('applicant/<int:pk>/resume/',
         ApplicantResume.as_view(), name='applicant-resume'),
    path('applicant/<int:pk>/image/',
         ApplicantImage.as_view(), name='applicant-image'),
    path('applicant/<int:pk>/application/',
         ApplicantApplication.as_view(), name='applicant-application'),


    path('domain/create/', DomainCreate.as_view(), name='domain-create'),
    path('domain/', DomainList.as_view(), name='domain-list'),
    path('domain/<int:pk>/', DomainGet.as_view(), name='domain-get'),
    path('domain/<int:pk>/update/',
         DomainUpdate.as_view(), name='domain-update'),
    path('domain/<int:pk>/application/',
         DomainApplication.as_view(), name='domain-application'),


    path('application/create/', ApplicationCreate.as_view(),
         name='application-create'),
    path('application/', ApplicationList.as_view(), name='application-list'),
    path('application/<int:pk>/', ApplicationDetail.as_view(),
         name='application-detail'),
    path('application/<int:pk>/update/', ApplicationUpdate.as_view(),
         name='application-update'),


    path('skill/', SkillList.as_view(), name='skill-list'),
    path('skill/<int:pk>/', SkillDetail.as_view(), name='skill-detail'),
]

app_name = 'jobportal'
