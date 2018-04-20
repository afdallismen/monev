from django.db import models

from region.models import Province, Regency


class Diklat(models.Model):
    title = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    regency = models.ManyToManyField(Regency)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    duration = models.PositiveSmallIntegerField()
    supervisor = models.CharField(max_length=200)
    participants = models.PositiveSmallIntegerField()

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
        return "Questionnaire {} from {}".format(
            self.get_instrument_display(),
            self.diklat
        )


class Topic(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return str(self.title).title()


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return str(self.text).capitalize()
