from django.db import models


class Subnews(models.Model):
    content = models.TextField(verbose_name="محتوا")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'زیرخبر'
        verbose_name_plural = 'زیرخبرها'