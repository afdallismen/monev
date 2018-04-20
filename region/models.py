from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "province"
        verbose_name_plural = "provincies"

    def __str__(self):
        return str(self.name)


class Regency(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "regency"
        verbose_name_plural = "regencies"

    def __str__(self):
        return str(self.name)
