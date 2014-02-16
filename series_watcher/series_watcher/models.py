# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Series(models.Model):
    name = models.CharField(max_length=100)
    url_keyword = models.CharField(max_length=30)
    synopsis = models.TextField(blank=True)
    genre = models.CharField(max_length=30, blank=True)
    release_date = models.CharField(blank=True, max_length=30)
    photo = models.URLField(blank=True)
    imdb = models.URLField(blank=True)
    url = models.URLField(blank=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name


class Season(models.Model):
    number = models.PositiveSmallIntegerField()
    series = models.ForeignKey(Series)

    def __unicode__(self):
        return "%s Season %d" % (self.series.name, self.number)


class Episode(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    real_number = models.CharField(max_length=5)
    season = models.ForeignKey(Season)
    url = models.URLField(blank=True)
    watchers = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        if self.name:
            return u"%s Season %d Episode %s – %s" % (
                self.season.series.name, self.season.number,
                self.real_number, self.name)
        else:
            return u"%s Season %d Episode %s" % (
                self.season.series.name, self.season.number,
                self.real_number)
