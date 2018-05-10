from django.db import models
from django.utils.translation import gettext_lazy as _


from account.models import Respondent
from region.models import Province, Regency


class Diklat(models.Model):
    title = models.CharField(_("title"), max_length=200)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_("province"),
    )
    regencies = models.ManyToManyField(Regency, verbose_name=_("regencies"))
    date = models.DateTimeField(_("date"))
    location = models.CharField(_("location"), max_length=200)
    duration = models.PositiveSmallIntegerField(_("duration"))
    supervisor = models.CharField(_("supervisor"), max_length=200)
    num_of_participant = models.PositiveSmallIntegerField(
        _("num of participant"))

    class Meta:
        verbose_name = _("diklat")
        verbose_name_plural = _("diklat")

    def __str__(self):
        return str(self.title)


class Questionnaire(models.Model):
    INSTRUMENT_CHOICES = (
        ('instrument_a', _("Instrument A")),
        ('instrument_b', _("Instrument B")),
        ('instrument_c', _("Instrument C")),
        ('instrument_d', _("Instrument D")),
        ('instrument_e', _("Instrument E")),
    )

    diklat = models.ForeignKey(
        Diklat,
        on_delete=models.CASCADE,
        verbose_name=_("diklat"),
    )
    title = models.CharField(_("title"), max_length=200)
    instrument = models.CharField(
        _("instrument"),
        max_length=12,
        choices=INSTRUMENT_CHOICES,
    )

    class Meta:
        unique_together = ('diklat', 'instrument')
        verbose_name = _("questionnaire")
        verbose_name_plural = _("questionnaires")

    def __str__(self):
        return str(self.title)


class Topic(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        verbose_name=_("questionnaire"),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("parent")
    )
    title = models.CharField(_("title"), max_length=200)

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return str(self.title)


TYPE_CHOICES = (
    ('essay', _("Essay")),
    ('objective', _("Objective")),
    ('group_of_objective', _("Group of objective")),
)


class Question(models.Model):
    TYPE_CHOICES = TYPE_CHOICES

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=("topic"),
    )
    type = models.CharField(_("type"), max_length=18, choices=TYPE_CHOICES)
    text = models.TextField(_("text"), blank=True, default="")
    with_recommendation = models.BooleanField(
        _("with recommendation"),
        default=True,
    )
    index_as_table_head = models.BooleanField(
        _("index as table head"),
        default=False,
    )

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        if self.text:
            return str(self.text)
        else:
            return _("Question{!s} for topic{!s}").format(
                self.id, self.topic)


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        limit_choices_to={'type__in': ['objective', 'group_of_objective']},
        verbose_name=_("option"),
    )
    name = models.CharField(_("name"), max_length=200)
    code = models.CharField(_("code"), max_length=5)

    class Meta:
        verbose_name = _("option")
        verbose_name_plural = _("options")

    def __str__(self):
        return str(self.name)


class Measure(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        limit_choices_to={'type__in': ['objective', 'group_of_objective']},
        verbose_name=_("question"),
    )
    name = models.TextField(_("name"), max_length=200)

    class Meta:
        verbose_name = _("measure")
        verbose_name_plural = _("measures")

    def __str__(self):
        return str(self.name)


class Response(models.Model):
    TYPE_CHOICES = TYPE_CHOICES

    respondent = models.ForeignKey(
        Respondent,
        on_delete=models.CASCADE,
        verbose_name=_("respondent"),
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("question"),
    )
    type = models.CharField(_("type"), max_length=18, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = _("response")
        verbose_name_plural = _("responses")

    def type_is(self, type):
        has_relation = hasattr(
            self, '{}response'.format(type.replace("_", "")))
        if self.type == type and has_relation:
            return True
        return False

    def __str__(self):
        if self.type_is('essay'):
            return str(self.essayresponse.text)
        elif self.type_is('objective'):
            return str(self.objectiveresponse.selected)
        elif self.type_is('group_of_objective'):
            return str(self.groupofobjectiveresponse.selected)
        else:
            return _("Undefined response{}").format(self.id)


class EssayResponse(models.Model):
    response = models.OneToOneField(
        Response,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'essay'},
        verbose_name=_("response"),
    )
    text = models.TextField(_("text"))

    class Meta:
        verbose_name = _("essay response")
        verbose_name_plural = _("essay responses")

    def __str__(self):
        return self.text


class ObjectiveResponse(models.Model):
    response = models.OneToOneField(
        Response,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'objective'},
        verbose_name=_("response"),
    )
    selected = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name=_("selected"),
    )

    class Meta:
        verbose_name = _("objective response")
        verbose_name_plural = _("objective responses")

    def __str__(self):
        return self.selected


class GroupOfObjectiveResponse(models.Model):
    response = models.OneToOneField(
        Response,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'group_of_objective'},
        verbose_name=_("response")
    )
    measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        verbose_name=_("measure"),
    )
    selected = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name=_("selected"),
    )

    class Meta:
        verbose_name = _("group of objective response")
        verbose_name_plural = _("group of objective responses")

    def __str__(self):
        return self.selected


class Recommendation(models.Model):
    respondent = models.ForeignKey(
        Respondent,
        on_delete=models.CASCADE,
        verbose_name=_("respondent"),
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("question"),
    )
    text = models.TextField(_("text"), blank=True, default="")

    class Meta:
        unique_together = ('respondent', 'question')
        verbose_name = _("recommendation")
        verbose_name_plural = _("recommendations")

    def __str__(self):
        return str(self.text)
