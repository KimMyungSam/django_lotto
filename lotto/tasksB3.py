from pandas import pandas as pd
import numpy as np
import random
from statsmodels.tsa.arima_model import ARIMA

from django.utils import timezone
from .models import ShootNumbers, DecidedNumbers, FormInput
# asynchronuous task
from celery import task

# form input에서 받아온 shooter, shot_count값 추출함. ORM에 추출한 조합을 저장함.
@task
def taskB3():
    df = pd.DataFrame(list(FormInput.objects.values()))
    FrominputShooter = df['shooter'].iloc[-1] # shooter
    FrominputShotCount = df['shot_count'].iloc[-1]  # shot_count

    # 5밴드 2연속 7번, 4밴드 7연속 6번, 8,9연속 1번, 3밴드 4연속 5번, 2밴드 1연속만 있음.
    df = pd.DataFrame(list(DecidedNumbers.objects.values('shotDate','band')))  # qury set를 dataframe으로 변환
    df_band_ts = df.sort_values(by='shotDate', ascending=False)  # 날짜를 기준으로 내림차순으로 정렬
    df_band_ts = df_band_ts.set_index('shotDate')

    # ARIMA로 목표 값과 std값을 뽑아내기위해, df_total dataframe 만듬.
    df_total = pd.DataFrame(list(DecidedNumbers.objects.values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
    df_total = df_total.set_index('shotDate')
    predict_total_value, predict_total_25, predict_total_75 = predict_nums(df_total, band)  #band별 ARIMA로 total값 예측

    origin_nums = list()
    except_nums = list()

    # band3 알고리즘
    time_index = 25  # band=3 최근 50회중 나오지 않는 번호는 제외
    df_band = pd.DataFrame(list(DecidedNumbers.objects.values\
              ('count','one','two','three','four','five','six','shotDate','total', 'band')))
    nums = analysis(df_band, time_index, band)

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
        nums = shot(origin_nums, band, predict_total_value, predict_total_25, predict_total_75, count)
        unique_elements, counts_elements = np.unique(nums, return_counts=True)
        origin15_nums = unique_elements.tolist()
        n15 = len(unique_elements)
        count += 1  # 추첨 5개 조합으로 15개 이상 번호가 추출되지 않으면 조합을 1개씩 증가시킴

    # 당첨번호 추출하기
    # shot_count = 5 #Default값으로 5개 조합
    lottos = shot(origin15_nums, band, predict_total_value, predict_total_25, predict_total_75, FrominputShotCount)
    # detail 페이지에서 조합별로 출력되도록 text로 변환함
    lotto_str = ""
    for lotto in lottos:
        lotto_str += str(lotto)+'\n'

    #ORM 저장
    shootnumbers = ShootNumbers (
        shooter = FrominputShooter,
        shot_count = FrominputShotCount,
        update_date = timezone.now(),
        lottos = lotto_str,
        predict_total_value = predict_total_value,
        predict_total_25 = predict_total_25,
        predict_total_75 = predict_total_75,
        origin_nums = str(origin_nums),
        except_nums = str(except_nums),
        band = band)
    shootnumbers.save()

@task
def taskB4():
    df = pd.DataFrame(list(FormInput.objects.values()))
    FrominputShooter = df['shooter'].iloc[-1] # shooter
    FrominputShotCount = df['shot_count'].iloc[-1]  # shot_count

    # 5밴드 2연속 7번, 4밴드 7연속 6번, 8,9연속 1번, 3밴드 4연속 5번, 2밴드 1연속만 있음.
    df = pd.DataFrame(list(DecidedNumbers.objects.values('shotDate','band')))  # qury set를 dataframe으로 변환
    df_band_ts = df.sort_values(by='shotDate', ascending=False)  # 날짜를 기준으로 내림차순으로 정렬
    df_band_ts = df_band_ts.set_index('shotDate')

    # ARIMA로 목표 값과 std값을 뽑아내기위해, df_total dataframe 만듬.
    df_total = pd.DataFrame(list(DecidedNumbers.objects.values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
    df_total = df_total.set_index('shotDate')
    predict_total_value, predict_total_25, predict_total_75 = predict_nums(df_total, band)  #band별 ARIMA로 total값 예측

    origin_nums = list()
    except_nums = list()

    # band4 알고리즘
    time_index = 25 # band=4 최근 25회중 나오지 않는 번호는 제외
    df_band = pd.DataFrame(list(DecidedNumbers.objects.values\
              ('count','one','two','three','four','five','six','shotDate','total', 'band')))
    nums = analysis(df_band, time_index, band)

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
        nums = shot(origin_nums, band, predict_total_value, predict_total_25, predict_total_75, count)
        unique_elements, counts_elements = np.unique(nums, return_counts=True)
        origin15_nums = unique_elements.tolist()
        n15 = len(unique_elements)
        count += 1  # 추첨 5개 조합으로 15개 이상 번호가 추출되지 않으면 조합을 1개씩 증가시킴

    # 당첨번호 추출하기
    # shot_count = 5 #Default값으로 5개 조합
    lottos = shot(origin15_nums, band, predict_total_value, predict_total_25, predict_total_75, FrominputShotCount)
    # detail 페이지에서 조합별로 출력되도록 text로 변환함
    lotto_str = ""
    for lotto in lottos:
        lotto_str += str(lotto)+'\n'

    #ORM 저장
    shootnumbers = ShootNumbers (
        shooter = FrominputShooter,
        shot_count = FrominputShotCount,
        update_date = timezone.now(),
        lottos = lotto_str,
        predict_total_value = predict_total_value,
        predict_total_25 = predict_total_25,
        predict_total_75 = predict_total_75,
        origin_nums = str(origin_nums),
        except_nums = str(except_nums),
        band = band)
    shootnumbers.save()

# ARIAM를 통한 total 번호 예측, 결과는 preditc num와 std값을 반환
def predict_nums(df, band):
    data = df[df.band == band]
    X = data['total']

    size = int(len(X) * 0.85)
    train, test = X[0:size], X[size:len(X)]
    test = np.append(test, 135) # predict를 위한 추가 기준값

    # non- stationary
    history = [float(x) for x in train]
    predictions = list()
    diff = list()

    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast(alpha=1)
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        diff.append(yhat - obs)

    df = pd.DataFrame(diff)
    diff = df.describe()
    return (int(predictions[-1]), int(diff[0].loc['25%']), int(diff[0].loc['75%']))

# band별 최근횟수 번호들의 count를 구하고, 제외번호를 뽑음
def analysis(df_band, time_index, band=3):
    df_band = df_band.sort_values(by='shotDate', ascending=False)  # 날짜를 기준으로 내림차순으로 정렬

    #1부터 45까지의 배열을 생성하고 0으로 초기화
    lottoarray = [0 for i in range(0,46)]
    df_list = df_band[(df_band['band'] == band)]
    df_list = df_list.reset_index()
    results = df_list.loc[0:time_index,['one','two','three','four','five','six']]

    for index, row in results.iterrows():
        for i in range(6):
            k = row[i]
            count = lottoarray[k]
            lottoarray[k] = count + 1

    return (lottoarray)

# 각 조건에 맞게 arima predict nums와 except_nums를 포함하여 번호 조합을 만듬.
def shot(origin_nums, targetBand, predict_total_value, predict_25, predict_75, shot_count):
    df_quantile = pd.DataFrame(list(DecidedNumbers.objects.values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
    quantile_max, quantile_min = quantile_analysis(df_quantile)  #분위수 max, min값 구함

    winNumber = []
    gen_count = 0  #
    result = 0  # 난수 발생후 저장변수 0으로 초기화
    ConditionCount = 0
    # 제외건수
    drop = 0
    drop2 = 0
    drop3 = 0
    drop4 = 0

    while True:  # 예측 조합 추출후 break로 종료

        lotto_continue = 0  # 연번 변수 0으로 초기화
        band = 0  #밴드
        yellow = 0  # 1~10숫자 색
        blue = 0  # 11~20숫자 색
        red = 0  # 21~30숫자 색
        green = 0  # 31~40숫자 색
        gray = 0  # 41 ~ 45숫자 색

        result = sorted(random.sample(origin_nums,6))  # 예측번호로 부터 6개 뽑아내기

        # band 구분하기
        for i in range(0,6):
            if (result[i] <= 10):
                yellow += 1
            elif (result[i] >= 11 and result[i] <= 20):
                blue += 1
            elif (result[i] >= 21 and result[i] <= 30):
                red += 1
            elif (result[i] >= 31 and result[i] <= 40):
                green += 1
            elif (result[i] >= 41 and result[i] <= 45):
                gray += 1

        #band 카운트
        if (yellow > 0):  band += 1
        if (blue > 0):  band += 1
        if (red > 0):   band += 1
        if (green > 0): band += 1
        if (gray > 0):  band += 1

        # 번호 6개의 sum 값 구하기
        total = sum(result[0:6])

        #3자리 연번이상 확인하기
        if (result[3] - result[0] == 3):  #4 연번
            lotto_continue += 1
        elif (result[4] - result[1] == 3):
            lotto_continue += 1
        elif (result[5] - result[2] == 3):
            lotto_continue += 1
        elif (result[4] - result[0] == 4):  #5 연번
            lotto_continue += 1
        elif (result[5] - result[1] == 4):
            lotto_continue += 1

        # odd, even count 구하기
        even = 0
        odd = 0
        for i in result:
            if i%2 == 0:
                even += 1
            elif  i%2 != 0:
                odd += 1

        # 모든 조건을 검증후 번호 추출
        if targetBand == band:  # 3,4 밴드등 목표 밴드 확인
            if (total <= quantile_max) and (total >= quantile_min):  # 분위수 range외 제외
                if lotto_continue == 0:  #4,5 연속번호 조합은 제외
                    ConditionCount += 1
                    if ConditionCount > random.randint(100000,1000000):  #십만에서 백만중 하나 추출하여 count횟수가 그만큼 클때 인정
                        if (odd < 6 and even < 6):  # 홀/짝수 갯수가 6이상이면 제외
                            # print ("odd_even=",drop)
                            # print ("ConditionCount=",ConditionCount)
                            # print ("continue=",drop2)
                            # print ("quantile=",drop3)
                            # print ("band비교=",drop4)
                            # print ("")
                            # 변수 초기화
                            ConditionCount = 0
                            drop = 0
                            drop2 = 0
                            drop3 = 0
                            drop4 = 0
                            # 조합 건수 카운트
                            gen_count += 1

                            # 당첨번호
                            winNumber.append(result)
                        else:  drop += 1
                else:  drop2 += 1
            else:  drop3 += 1
        else:  drop4 += 1

        if (gen_count > (shot_count -1)):  # 추출한 조합 수를 기준으로 while문 실행행
            break

    return winNumber

# 분위수 구하기
def quantile(x,p):
    p_index = int(p * len(x))
    return sorted(x)[p_index]

# 분위수 범위안의 숫자를 count함.
def quantile_count(total_val, maxi, mini):
    count = 0

    for num in total_val:
        if (num >= mini and num <= maxi):
            count += 1
    return count

# quantile를 구하고 quantile 0.90, 0.10  수준의 max, min 값을 구함
# 당첨번호 6개의 sum(total)으로 분석함.
def quantile_analysis(df_quantile):
    df = df_quantile
    df = df.sort_values(by='shotDate', ascending=False)
    df = df.reset_index()
    df_total = df.loc[0:100,['total']]  # 100열, total 데이터 뽑아냄
    total_val = df_total.values
    return (quantile(total_val, 0.90), quantile(total_val, 0.1))
