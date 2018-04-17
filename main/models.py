from django.core import validators
from django.db import models
from django.utils import timezone

from region.utils import PROVINCES, REGENCIES


class Diklat(models.Model):
    PROVINCE_CHOICES = [[row['id'], row['name']] for row in PROVINCES]
    REGENCY_CHOCIES = [[row['id'], row['name']] for row in REGENCIES]

    title = models.CharField(max_length=200)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)
    regency = models.CharField(max_length=4, choices=REGENCY_CHOCIES)
    date = models.DateTimeField(
        validators=[
            validators.MinValueValidator(
                timezone.now(),
                "Date can't be in the past."
            ),
        ]
    )
    location = models.CharField(max_length=200)
    duration = models.PositiveSmallIntegerField()
    supervisor = models.CharField(max_length=200)
    participants = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "diklat"
        verbose_name_plural = "diklat"

    def __str__(self):
        return str(self.title).capitalize()


class Questionnaire(models.Model):
    INSTRUMENT_CHOICES = (
        ('0', "instrument A"),
        ('1', "instrument B"),
        ('2', "instrument C"),
    )

    diklat = models.ForeignKey(Diklat, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=2, choices=INSTRUMENT_CHOICES)

    class Meta:
        verbose_name = "questionnaire"
        verbose_name_plural = "questionnaires"

    def __repr__(self):
        return "Questionnaire(instrument={}, diklat={})".format((
            self.get_instrument_display(),
            self.diklat
        ))


class Topic(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return str(self.title).capitalize()


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
