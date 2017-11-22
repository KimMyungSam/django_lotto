from django.db import models
from django.utils import timezone
import random
import pandas as pd

# Create your models here.
class ShootNumbers(models.Model):
    name = models.CharField(max_length = 24)
    # lottos = models.CharField(max_length = 255, default = '[1,2,3,4,5,6]')
    lottos = models.TextField(default = '[1,2,3,4,5,6]')
    text = models.CharField(max_length = 24)
    shoot_lotto = models.IntegerField(default = 5)
    update_date = models.DateTimeField()

    class Meta:
        ordering = ['-update_date']

    def __str__(self):
        return "%s %s" % (self.name, self.text)

class DecidedNumbers(models.Model):
    count = models.IntegerField()
    shotDate = models.DateField()
    one = models.IntegerField()
    two = models.IntegerField()
    three = models.IntegerField()
    four = models.IntegerField()
    five = models.IntegerField()
    six = models.IntegerField()
    bonus = models.IntegerField()
    person = models.IntegerField()
    amount = models.CharField(max_length = 24, default = '1000')
    total = models.IntegerField()
    odd = models.IntegerField()
    even = models.IntegerField()
    yellow = models.IntegerField()
    blue = models.IntegerField()
    red = models.IntegerField()
    green = models.IntegerField()
    gray = models.IntegerField()
    band = models.IntegerField()
    one_continue = models.IntegerField()
    two_continue = models.IntegerField()
    three_continue = models.IntegerField()
    four_continue = models.IntegerField()
    end_digit = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['shotDate'])
        ]

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s %s"\
        %(self.count, self.shotDate, self.one, self.two, self.three, self.four, self.five, self.six, self.total, self.band)
