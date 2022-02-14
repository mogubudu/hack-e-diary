from random import choice
from datacenter.models import (Schoolkid, Mark,
                               Chastisement, Lesson, Commendation)


def fix_marks(full_name):
    schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(full_name):
    schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    notes = Chastisement.objects.filter(schoolkid=schoolkid)
    notes.delete()


def create_commendation(full_name, lesson):
    schoolkid = Schoolkid.objects.get(
        full_name__contains=full_name
        )
    child_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
        )
    lesson = child_lessons.filter(
        subject__title=lesson
        ).order_by('date').first()

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
