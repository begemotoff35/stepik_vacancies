from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.db.models import Count
from django.http import Http404

from vacancies.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = "vacancies/index.html"

    def get(self, request, *args, **kwargs):
        #
        # Сделано криво, подскажите пожалуйста в рецензии, как правильно!
        #
        # Все вакансии из нашей базы данных:
        all_specialties = Specialty.objects.all()
        # Группируем специальности из вакансий:
        vacant_specialties = Vacancy.objects.values('specialty').annotate(count=Count('specialty'))
        for spec in vacant_specialties:
            all_spec = all_specialties.filter(id=spec['specialty']).first()
            if all_spec is not None:
                # Добавляем поля для шаблона:
                spec['code'] = all_spec.code
                spec['title'] = all_spec.title
                spec['picture'] = all_spec.picture

        # все компании:
        all_companies = Company.objects.all()
        # из вакансий:
        vacant_companies = Vacancy.objects.values('company').annotate(count=Count('specialty'))
        for company in vacant_companies:
            all_comp = all_companies.filter(id=company['company']).first()
            if all_comp is not None:
                # Добавляем поля для шаблона:
                company['name'] = all_comp.name
                company['logo'] = all_comp.logo

        return render(request, self.template_name, {'specialties': vacant_specialties, 'companies': vacant_companies})


class VacanciesView(TemplateView):
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        speciality_code = context.get('speciality_code', None)
        if speciality_code is None:
            vacancies = Vacancy.objects.all()
        else:
            specialty = Specialty.objects.filter(code=speciality_code).first()
            vacancies = Vacancy.objects.filter(specialty__code=speciality_code)
            if specialty is None:
                raise Http404

            context['current_specialty'] = specialty

        context['vacancies'] = vacancies

        return context


class VacancyView(TemplateView):
    template_name = "vacancies/vacancy.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title_left': 'Вакансия'})


class CompanyView(TemplateView):
    template_name = "vacancies/company.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title_left': 'Компания'})
