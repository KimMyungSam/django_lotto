from django.db import models
from django.utils import timezone
import random
import pandas as pd
import numpy as np

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='update_date')

class FormInput(models.Model):
    shooter = models.CharField(max_length = 255)  # 추출할때 문구
    shot_count = models.IntegerField(default = 5)  # 추천할 조합 갯수
    # object 값을 가져갈때 form save 액션일어 날때 shooter와 shot_count 값을 얻고자 함.
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.shooter, self.shot_count)

# Create your models here.
class ShootNumbers(models.Model):
    # use a PublishedManager of pagination function
    objects = models.Manager()  # The default Manager
    updated_date = PublishedManager()  # Our custom manager.

    # lottos = models.CharField(max_length = 255, default = '[1,2,3,4,5,6]')
    lottos = models.TextField(default = '[1,2,3,4,5,6]')  # Guess번호를 저장하는 텍스트 필드
    shooter = models.CharField(max_length = 255)  # 추출할때 문구
    shot_count = models.IntegerField(default = 5)  # 추천할 조합 갯수
    update_date = models.DateTimeField(auto_now_add=True)
    predict_total_value = models.IntegerField(default = 0)  # 시계열을 통한 total추정 값
    predict_total_25 = models.IntegerField(default = 0)  #시계열을 통한 total추정값의 25%
    predict_total_75 = models.IntegerField(default = 0)  #시계열을 통한 total추정값의 75%
    origin_nums = models.CharField(max_length = 255)  # 추천에 사용할 번호
    except_nums = models.CharField(max_length = 255)  # 제외번호 지정
    band = models.IntegerField(default = 0)  # 분석 band

    class Meta:
        ordering = ['-update_date']

    def __str__(self):
        return "%s %s" % (self.shooter, self.lottos)

class DecidedNumbers(models.Model):
    count = models.IntegerField(default = 0)
    shotDate = models.DateField()
    one = models.IntegerField(default = 0)
    two = models.IntegerField(default = 0)
    three = models.IntegerField(default = 0)
    four = models.IntegerField(default = 0)
    five = models.IntegerField(default = 0)
    six = models.IntegerField(default = 0)
    bonus = models.IntegerField(default = 0)
    person = models.IntegerField(default = 0)
    amount = models.CharField(max_length = 24, default = '1000')
    total = models.IntegerField(default = 0)
    odd = models.IntegerField(default = 0)
    even = models.IntegerField(default = 0)
    yellow = models.IntegerField(default = 0)
    blue = models.IntegerField(default = 0)
    red = models.IntegerField(default = 0)
    green = models.IntegerField(default = 0)
    gray = models.IntegerField(default = 0)
    band = models.IntegerField(default = 0)
    one_continue = models.IntegerField(default = 0)
    two_continue = models.IntegerField(default = 0)
    three_continue = models.IntegerField(default = 0)
    four_continue = models.IntegerField(default = 0)
    end_digit = models.IntegerField(default = 0)

    class Meta:
        indexes = [
            models.Index(fields=['shotDate'])
        ]

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s %s"\
        %(self.count, self.shotDate, self.one, self.two, self.three, self.four, self.five, self.six, self.total, self.band)
