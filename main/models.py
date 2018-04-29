from django.db import models

from account.models import Respondent
from region.models import Province, Regency


class Diklat(models.Model):
    title = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    regency = models.ManyToManyField(Regency)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    duration = models.PositiveSmallIntegerField()
    supervisor = models.CharField(max_length=200)
    respondents = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "diklat"
        verbose_name_plural = "diklat"

    def __str__(self):
        return str(self.title).title()


class Questionnaire(models.Model):
    INSTRUMENT_CHOICES = (
        ('0', "Instrument A"),
        ('1', "Instrument B"),
        ('2', "Instrument C"),
    )

    diklat = models.ForeignKey(Diklat, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=2, choices=INSTRUMENT_CHOICES)

    class Meta:
        unique_together = ('diklat', 'instrument')
        verbose_name = "questionnaire"
        verbose_name_plural = "questionnaires"

    def __str__(self):
        return "Questionnaire {} from diklat {}".format(
            self.get_instrument_display(),
            self.diklat
        )


class Topic(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"

    def __str__(self):
        return str(self.title).title()


class Question(models.Model):
    TYPE_CHOICES = (
        ("0", "essay"),
        ("1", "objective"),
        ("2", "group of objective"),
    )

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    text = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return str(self.text).capitalize()


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        limit_choices_to={'type__in': ['1', '2']},
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "option"
        verbose_name_plural = "options"

    def __str__(self):
        return str(self.name).capitalize()


class Measure(models.Model):
    question = models.ForeignKey(
        Question,
        limit_choices_to={'type__in': ['2', '3']},
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "measure"
        verbose_name_plural = "measures"

    def __str__(self):
        return str(self.name).capitalize()


class Response(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(
        null=True,
        blank=True,
    )
    measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    selected = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "response"
        verbose_name_plural = "responses"

    def __str__(self):
        return "{!s} respond for question '{!s}'".format(
            self.respondent,
            self.question,
        )


class Recommendation(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "recommendation"
        verbose_name_plural = "recommendations"

    def __str__(self):
        return "{!s} recommendation for question {!s}".format(
            self.respondent, self.question)
