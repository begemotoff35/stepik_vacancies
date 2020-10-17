from django.db import models


class Specialty(models.Model):
    code = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    picture = models.FileField()

    def __str__(self):
        return f'{self.code}/{self.title}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.FileField()
    description = models.TextField(max_length=200)
    employee_count = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies", null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies", null=True)
    skills = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()

