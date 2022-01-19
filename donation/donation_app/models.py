from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPES = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna'),
    )

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.SmallIntegerField(choices=TYPES, default=1, max_length=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}: {self.get_type_display()}'
