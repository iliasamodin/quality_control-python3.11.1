from django.db import models


class Concentrate(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    iron = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        default=0,
        blank=True
    )
    silicon = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        default=0,
        blank=True
    )
    aluminum = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        default=0,
        blank=True
    )
    calcium = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        default=0,
        blank=True
    )
    sulfur = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        default=0,
        blank=True
    )

    class Meta:
        ordering = ["-year", "-month", "name"] 
        unique_together = ["name", "year", "month"]

    def __str__(self):
        return f"{self.name} {self.year}.{self.month}"
