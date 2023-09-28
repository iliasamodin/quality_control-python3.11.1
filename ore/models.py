from django.db import models


class Concentrate(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    iron = models.DecimalField(max_digits=7, decimal_places=4)
    silicon = models.DecimalField(max_digits=7, decimal_places=4)
    aluminum = models.DecimalField(max_digits=7, decimal_places=4)
    calcium = models.DecimalField(max_digits=7, decimal_places=4)
    sulfur = models.DecimalField(max_digits=7, decimal_places=4)

    class Meta:
        ordering = ["-year", "-month", "name"] 
        unique_together = ["name", "year", "month"]

    def __str__(self):
        return f"{self.name} {self.year}.{self.month}"
