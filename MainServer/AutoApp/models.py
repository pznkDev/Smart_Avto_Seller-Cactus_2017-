from django.db import models

# Create your models here.


class Mark(models.Model):
    value_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Model(models.Model):
    value_id = models.CharField(max_length=200)
    mark_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Region(models.Model):
    value_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
