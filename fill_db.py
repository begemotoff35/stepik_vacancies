# Заполняем нашу базу данных в соответствии с данными из файла data.py

import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_vacancies.settings'
django.setup()  # Всякие Django штуки импортим после сетапа

from vacancies.models import Vacancy, Company, Specialty
from vacancies.data import jobs, companies, specialties


if __name__ == '__main__':
    for spec in specialties:
        print(spec['code'])

