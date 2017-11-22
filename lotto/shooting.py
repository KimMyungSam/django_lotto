from pandas import datetime
from pandas import pandas as pd
import numpy as np

from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
# ShootNumets 번호예측 저장하는 모델, DecidedNumbers 로또번호 크롤링후 저장하는 모델
from django.db.models import Max
from .models import ShootNumbers, DecidedNumbers
from django.utils import timezone

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
    return (int(predictions[-1]), int(diff[0].loc['std']))

def analysis(time_index, band=3):
    df_band = pd.DataFrame(list(DecidedNumbers.objects.all().values\
    ('count','one','two','three','four','five','six','shotDate','total', 'band')))
    latest_time = DecidedNumbers.objects.all().aggregate(Max('count'))

    #1부터 45까지의 배열을 생성하고 0으로 초기화
    lottoarray = [0 for i in range(0,46)]
    df_list = df_band[(df_band['band'] == band) & (df_band['count'] > 600)]
    # results = df_band[(df_band['band'] == band) & (df_band['count'] > 100),'one','two','three','four','five','six']
    results = df_list.loc[:,['one','two','three','four','five','six']]

    for index, row in results.iterrows():
        k = row[0]
        count = lottoarray[k]
        lottoarray[k] = count + 1

    print ("전체 숫자 당첨 카운수")
    for i in range(1, len(lottoarray)):
        if (i % 10) == 0:
                print("")  # 10개 마다 줄 바꾸기
        print("[" + str(i) + ":" + str(lottoarray[i]) + "]", end=" ")
    return (lottoarray)

# 로또 번호 생성 및 데이터베이스 저장, main part
def generate():
    # ARIMA로 목표 값과 std값을 뽑아냄
    df_total = pd.DataFrame(list(DecidedNumbers.objects.all().values('shotDate','total', 'band')))  # qury set를 dataframe으로 변환
    df_total = df_total.set_index('shotDate')
    for band in [3,4]:
        if band == 3:
            b3_predict_value, b3_predict_std = predict_nums(df_total, band)  #ARIMA를 결과를 변수에 저장
        elif band == 4:
            b3_predict_value, b3_predict_std = predict_nums(df_total, band)  #ARIMA를 결과를 변수에 저장

    # 최근번호중 제외수 선택, 45개 번호중 최근 미출현 번호를 제외함.
    b3_nums = []
    b4_nums = []
    for band in [3,4]:
        if band == 3:
            time_index = 50  # band=3 최근 50회중 나오지 않는 번호는 제외
            nums = analysis(time_index, band)
            except_nums = []
            for j in range(1,46):
                if nums[j] != 0:
                    b3_nums.append(j)
                else:
                    except_nums.append(j)
        elif band == 4:
            time_index = 25 # band=4 최근 25회중 나오지 않는 번호는 제외
            nums = analysis(time_index, band)
            except_nums = []
            for j in range(1,46):
                if nums[j] != 0:
                    b4_nums.append(j)
                else:
                    except_nums.append(j)
        print ("band{}, {}회 추첨중 zero count {}가 제외됨".format(band, time_index, except_nums))

    # 최근번호중 제외수 선택, 최근 10회 출현 번호중 최다 출현 횟수를 뽑고, 최다 횟수 출현번호 제외




    # for _ in range(0, ShootNumbers.shoot_lotto):
    #    random.shuffle(origin)
    #    guess = origin[:6]
    #    guess.sort()
    #    ShootNumbers.lottos += str(guess) +'\n'
    ShootNumbers.update_date = timezone.now()
    # ShootNumbers.save()
