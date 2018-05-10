from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']
        verbose_name = "province"
        verbose_name_plural = "provinces"

    def __str__(self):
        return str(self.name)


class Regency(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']
        verbose_name = "regency"
        verbose_name_plural = "regencies"

    def __str__(self):
        return str(self.name)
