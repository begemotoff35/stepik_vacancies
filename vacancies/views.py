from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainView(TemplateView):
    template_name = "vacancies/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class VacanciesView(TemplateView):
    template_name = "vacancies/vacancies.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title_left': 'Вакансии'})


class VacancyView(TemplateView):
    template_name = "vacancies/vacancy.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title_left': 'Вакансия'})


class CompanyView(TemplateView):
    template_name = "vacancies/company.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title_left': 'Компания'})
