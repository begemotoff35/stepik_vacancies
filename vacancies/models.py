from django.db import models


class Specialty(models.Model):
    code = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    picture = models.FileField()


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.FileField()
    description = models.TextField(max_length=200)
    employee_count = models.IntegerField()


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ManyToManyField(Specialty, related_name="vacancies")
    company = models.ManyToManyField(Company, related_name="vacancies")
    skills = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.CharField(max_length=100)

