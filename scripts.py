from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import (Schoolkid, Mark,
                               Chastisement, Lesson, Commendation)
from random import choice


def get_schoolkid(full_name):
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.DoesNotExist:
        print('Такого ученика не нашлось в базе, проверь на опечатки.')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников, попробуй уточнить запрос.')


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    notes = Chastisement.objects.filter(schoolkid=schoolkid)
    notes.delete()


def create_commendation(schoolkid, subject):
    child_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
    )

    lesson = child_lessons.filter(
        subject__title=subject
    ).order_by('date').first()

    if not lesson:
        print('Урока с таким названием нет')
        return

    commedations = ['Молодец!',
                    'Отлично!',
                    'Хорошо!',
                    'Великолепно!',
                    'Прекрасно!',
                    'Очень хороший ответ!']

    commedation = choice(commedations)
    Commendation.objects.create(schoolkid=schoolkid,
                                teacher=lesson.teacher,
                                subject=lesson.subject,
                                created=lesson.date,
                                text=commedation)
