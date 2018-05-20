from django.db import models


class BaseRegion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Province(BaseRegion):
    class Meta(BaseRegion.Meta):
        verbose_name = "province"
        verbose_name_plural = "provinces"


class Regency(BaseRegion):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta(BaseRegion.Meta):
        verbose_name = "regency"
        verbose_name_plural = "regencies"
