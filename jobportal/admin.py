from django.contrib import admin
from jobportal.models import Skill, Applicant, Domain, Application
# Register your models here.
admin.site.register(Skill)
admin.site.register(Applicant)
admin.site.register(Domain)
admin.site.register(Application)
