from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Applicant(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField(null=False)
    email = models.EmailField()
    image = models.ImageField()
    resume = models.FileField()
    linkedin_url = models.URLField()
    skills = models.ManyToManyField(Skill)
    description = models.TextField(max_length=500)
    achievements = models.TextField(max_length=500)
    experience = models.TextField(max_length=1000)
    education = models.TextField(max_length=1000)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Domain(models.Model):
    name = models.CharField(max_length=100)
    vacancies = models.IntegerField(default=0)
    skills_required = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32,
        choices=[('UNREVIEWED', 'UNREVIEWED'),
                 ('SELECTED', 'SELECTED'), ('REJECTED', 'REJECTED')],
        default='UNREVIEWED'
    )

    def __str__(self):
        return self.applicant.first_name + ' ' + self.applicant.last_name + ' | ' + self.domain.name
