from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm


class Movie(models.Model):
    """
    Class to store movie information
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Movie name', null=False, blank=False)
    rows = models.PositiveSmallIntegerField(default=100, verbose_name="Number of rows")
    columns = models.PositiveSmallIntegerField(default=100, verbose_name="Number of columns")


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'rows', 'columns']

TICKET_STATUS_CHOICES = (
    (1, 'AVAILABLE'),
    (2, 'BLOCKED'),
    (3, 'BOOKED')
)


class Tickets(models.Model):
    """
    Class to store movie tickets information
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_num = models.PositiveSmallIntegerField(null=False, blank=False)
    col_num = models.PositiveSmallIntegerField(null=False, blank=False)
    movie = models.ForeignKey(Movie, null=False)
    status = models.IntegerField(choices=TICKET_STATUS_CHOICES, default=1)
    session = models.CharField(blank=False, null=False, max_length=200)

    class Meta:
        unique_together = ('movie', 'row_num', 'col_num')


class TicketsForm(ModelForm):
    class Meta:
        model = Tickets
        fields = ['row_num', 'col_num',]