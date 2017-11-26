from django.db import models
from django.utils import timezone
import random
import pandas as pd
import numpy as np

from . import shooting

# Create your models here.
class ShootNumbers(models.Model):
    # lottos = models.CharField(max_length = 255, default = '[1,2,3,4,5,6]')
    lottos = models.TextField(default = '[1,2,3,4,5,6]')  # Guess번호를 저장하는 텍스트 필드
    shooter = models.CharField(max_length = 255)  # 추출할때 문구
    shot_count = models.IntegerField(default = 5)  # 추천할 조합 갯수
    update_date = models.DateTimeField()
    predict_total_value = models.IntegerField(default = 0)  # 시계열을 통한 total추정 값
    predict_total_25 = models.IntegerField(default = 0)  #시계열을 통한 total추정값의 25%
    predict_total_75 = models.IntegerField(default = 0)  #시계열을 통한 total추정값의 75%
    origin_nums = models.CharField(max_length = 255)  # 추천에 사용할 번호
    except_nums = models.CharField(max_length = 255)  # 제외번호 지정
    band = models.IntegerField(default = 0)  # 분석 band

    class Meta:
        ordering = ['-update_date']

    def generate(self):
        # ARIMA로 목표 값과 std값을 뽑아내기위해, df_total dataframe 만듬.
        df_total = pd.DataFrame(list(DecidedNumbers.objects.all().values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
        df_total = df_total.set_index('shotDate')
        # 최근번호중 제외수 선택, 45개 번호중 최근 미출현 번호를 제외함.

        for band in [3,4]:
            origin_nums = list()
            except_nums = list()
            predict_total_value, predict_total_25, predict_total_75 = shooting.predict_nums(df_total, band)  #band별 ARIMA로 total값 예측

            if band == 3:
                time_index = 25  # band=3 최근 50회중 나오지 않는 번호는 제외
                df_band = pd.DataFrame(list(DecidedNumbers.objects.all().values\
                          ('count','one','two','three','four','five','six','shotDate','total', 'band')))
                nums = shooting.analysis(df_band, time_index, band)

                for j in range(1,46):
                    if nums[j] != 0:
                        origin_nums.append(j)
                    else:
                        except_nums.append(j)

            elif band == 4:
                time_index = 25 # band=4 최근 25회중 나오지 않는 번호는 제외
                df_band = pd.DataFrame(list(DecidedNumbers.objects.all().values\
                          ('count','one','two','three','four','five','six','shotDate','total', 'band')))
                nums = shooting.analysis(df_band, time_index, band)

                for j in range(1,46):
                    if nums[j] != 0:
                        origin_nums.append(j)
                    else:
                        except_nums.append(j)

            # 당첨번호 만들기위한 15개 번호 추출하기
            n15 = 0  # 15개 버호추출을 위한 변수
            count = 3  # 번호 조합 추출 횟수
            origin15_nums = list()
            while n15 < 14:
                df_quantile = pd.DataFrame(list(DecidedNumbers.objects.all().values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
                nums = shooting.shot(origin_nums, band, predict_total_value, predict_total_25, predict_total_75, count, df_quantile)
                unique_elements, counts_elements = np.unique(nums, return_counts=True)
                origin15_nums = unique_elements.tolist()
                n15 = len(unique_elements)
                count += 1  # 추첨 5개 조합으로 15개 이상 번호가 추출되지 않으면 조합을 1개씩 증가시킴

            # 당첨번호 추출하기
            # shot_count = 5 #Default값으로 5개 조합
            lottos = shooting.shot(origin15_nums, band, predict_total_value, predict_total_25, predict_total_75, self.shot_count, df_quantile)
            lotto_char = ""
            for lotto in lottos:
                lotto_char = str(lotto) + '\n'
            #ORM 저장
            self.update_date = timezone.now()
            self.lottos = lotto_char
            self.predict_total_value = predict_total_value
            self.predict_total_25 = predict_total_25
            self.predict_total_75 = predict_total_75
            self.origin_nums = str(origin_nums)
            self.except_nums = str(except_nums)
            self.band = band
            self.save()

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
