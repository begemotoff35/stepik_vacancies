from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.db.models import Count
from django.http import Http404

from vacancies.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = "vacancies/index.html"

    def get(self, request, *args, **kwargs):
        #
        # Сделано через циклы. Подскажите, пожалуйста, в рецензии, как сделать одним запросом
        # и правильно передать данные в шаблон
        #
        # Список, в котором хранятся наши специальности и количество вакансий:
        specialties = list()

        all_specialties = list(Specialty.objects.all())
        # Группируем специальности из вакансий:
        vacant_specialties = Vacancy.objects.values('specialty').annotate(count=Count('specialty'))
        for specialty in all_specialties:
            number_of_vacancies = 0
            vacancy_set = vacant_specialties.filter(specialty=specialty.id)
            if len(vacancy_set):
                number_of_vacancies = vacancy_set[0]['count']
            specialties.append({"item": specialty, "number_of_vacancies": number_of_vacancies})

        # все компании:
        companies = list()

        all_companies = Company.objects.all()
        # из вакансий:
        vacant_companies = Vacancy.objects.values('company').annotate(count=Count('company'))
        for company in all_companies:
            number_of_vacancies = 0
            vacancy_set = vacant_companies.filter(company=company.id)
            if len(vacancy_set):
                number_of_vacancies = vacancy_set[0]['count']
            companies.append({"item": company, "number_of_vacancies": number_of_vacancies})

        return render(request, self.template_name, {'specialties': specialties, 'companies': companies})


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
        context['title_left'] = 'Вакансии'

        return context


class VacancyView(TemplateView):
    template_name = "vacancies/vacancy.html"

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = context.get('vacancy_id', None)
        if vacancy_id is None:
            raise Http404

        vacancy = Vacancy.objects.filter(id=vacancy_id).first()

        context['vacancy'] = vacancy
        context['title_left'] = 'Вакансия'

        return context


class CompanyView(TemplateView):
    template_name = "vacancies/company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = context.get('company_id', None)
        if company_id is None:
            raise Http404

        company = Company.objects.filter(id=company_id).first()
        vacancies = Vacancy.objects.filter(company_id=company_id)

        context['company'] = company
        context['vacancies'] = vacancies
        context['title_left'] = 'Компания'

        return context
