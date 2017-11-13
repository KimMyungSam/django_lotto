
# coding: utf-8

# ### 로또번호 추정하여 만들기 순서
# 1. 로또 홈페이지 크롤링
# 2. 최근 당첨번호 트랜드 분석
# 3. 번호 선정 로직 생성하기
# 4. random하게 번호 뽑기
# 4. 번호 선정후 1~45 경우수와 (결과)선정된 번호의 경우수 비교하기
# 5. 생성시마다 10개번호 산출

# <font color='red'>
#     <ul>
#         <li>1자리~6자리 합계 정규분포에서 상위 95%, 하위 5% 수준으로 분석시 max=188, min=84. 6개 숫자 합의 범위 188 ~ 84로 제한함(정규분포 90%만 인정)</li>
#         <li>홀수, 짝수 조합분석시 6개모두 홀수, 짝수 일 경우수는  1.82% 임으로 6개모두 짝/홀수 경우는 제외</li>
#         <li>color band는 3개 또는 4개 조합이 가장 높음.</li>
#         <li>연속번호 당첨 1,2조합, 1,2,3조합만.</li>
#         <li>동일한 끝자리수가 3회 이상인 조합은 버림 </li>
#     </ul>
# </font>

# <head>> describe winlotto;</head>
# <pre>
# +------------+-------------+------+-----+---------+-------+
# | Field      | Type        | Null | Key | Default | Extra |
# +------------+-------------+------+-----+---------+-------+
# | count      | int(10)     | NO   |     | NULL    |       |
# | 1          | int(2)      | NO   |     | NULL    |       |
# | 2          | int(2)      | NO   |     | NULL    |       |
# | 3          | int(2)      | NO   |     | NULL    |       |
# | 4          | int(2)      | NO   |     | NULL    |       |
# | 5          | int(2)      | NO   |     | NULL    |       |
# | 6          | int(2)      | NO   |     | NULL    |       |
# | 7          | int(2)      | NO   |     | NULL    |       |
# | persons    | int(2)      | NO   |     | NULL    |       |
# | amounts    | varchar(20) | NO   |     | NULL    |       |
# | total      | int(5)      | NO   |     | NULL    |       |
# | odd        | int(2)      | NO   |     | NULL    |       |
# | even       | int(2)      | NO   |     | NULL    |       |
# | yellow     | int(2)      | NO   |     | NULL    |       |
# | blue       | int(2)      | NO   |     | NULL    |       |
# | red        | int(2)      | NO   |     | NULL    |       |
# | green      | int(2)      | NO   |     | NULL    |       |
# | gray       | int(2)      | NO   |     | NULL    |       |
# | band       | int(2)      | NO   |     | NULL    |       |
# | 1continue  | int(2)      | NO   |     | NULL    |       |
# | 2continue  | int(2)      | NO   |     | NULL    |       |
# | 3continue  | int(2)      | NO   |     | NULL    |       |
# | 4continue  | int(2)      | NO   |     | NULL    |       |
# | endigDigit | int(2)      | NO   |     | NULL    |       |
# +------------+-------------+------+-----+---------+-------+
#  </pre>
# <pre>
# > select max(total), min(total) from winlotto where band=5 and count > 677;
# +------------+------------+
# | max(total) | min(total) |
# +------------+------------+
# |        177 |        122 |
# +------------+------------+
# 1 row in set (0.00 sec)
#
# > select max(total), min(total) from winlotto where band=4 and count > 677;
# +------------+------------+
# | max(total) | min(total) |
# +------------+------------+
# |        198 |         87 |
# +------------+------------+
# 1 row in set (0.00 sec)
#
# > select max(total), min(total) from winlotto where band=3 and count > 677;
# +------------+------------+
# | max(total) | min(total) |
# +------------+------------+
# |        203 |         50 |
# +------------+------------+
# 1 row in set (0.00 sec)
#
# > select max(total), min(total) from winlotto where band=2 and count > 677;
# +------------+------------+
# | max(total) | min(total) |
# +------------+------------+
# |        193 |         73 |
# +------------+------------+
# 1 row in set (0.00 sec)
# </pre>

#lotto.py

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import random

from .models import nums
from django.db.models import Max

#웹 크롤링 한 결과를 저장할 리스트
lotto_list = []

#로또 웹 사이트의 첫 주소
main_url = "http://www.nlotto.co.kr/gameResult.do?method=byWin"

#웹 크롤릴 주소
basic_url = "http://www.nlotto.co.kr/gameResult.do?method=byWin&drwNo="

def getLast():
    resp = requests.get(main_url)
    soup = BeautifulSoup(resp.text, "lxml")
    line = str(soup.find("meta", {"id" : "desc", "name" : "description"})['content'])

    begin = line.find(" ")
    end = line.find("회")

    if begin == -1 or end == -1:
        print("not found last lotto number")
        exit()
    return int(line[begin + 1 : end])

def checkLast():
    last = nums.objects.all().aggregate(Max('count'))
    if last['count__max'] is None:
        last['count__max'] = 0
    return last['count__max']

def crawler(fromPos,toPos):
    for i in range(fromPos,toPos + 1):
        crawler_url = basic_url + str(i)

        resp = requests.get(crawler_url)
        soup = BeautifulSoup(resp.text, "lxml")
        '''
        개발자 모드로 분석하여 HTML Tag로 찾을때
        div_data = soup.find_all('div', class_='lotto_win_number mt12')
        p_data = div_data[0].find_all('p',class_='number')
        img_number = p_data[0].find_all('img')
        '''
        line = str(soup.find("meta", {"id" : "desc", "name" : "description"})['content'])
        print("당첨회차: " + str(i))

        begin = line.find("당첨번호")
        begin = line.find(" ", begin) + 1
        end = line.find(".", begin)
        numbers = line[begin:end]
        print("당첨번호: " + numbers)

        begin = line.find("총")
        begin = line.find(" ", begin) + 1
        end = line.find("명", begin)
        persons = line[begin:end]
        print("당첨인원: " + persons)

        begin = line.find("당첨금액")
        begin = line.find(" ", begin) + 1
        end = line.find("원", begin)
        amount = line[begin:end]
        print("당첨금액: " + amount)

        info = {}
        info["회차"] = i
        info["번호"] = numbers
        info["당첨자"] = persons
        info["금액"] = amount

        lotto_list.append(info)
    return lotto_list


def insert(lotto_list):
    for dic in lotto_list:
        count = dic["회차"]
        numbers = dic["번호"]
        persons = dic["당첨자"]
        amounts = dic["금액"]
        odd = 0  # 홀수
        even = 0  # 짝수
        yellow = 0  # 1~10
        blue = 0  # 11~20
        red = 0  # 21~30
        green = 0  # 31~40
        gray = 0  # 41 ~ 45
        band = 0  #숫자 밴드 카운트
        one_continue = 0
        two_continue = 0
        three_continue = 0
        four_continue = 0
        winNumbers = []

        #print("insert to database at " + str(count))
        numberlist = str(numbers).split(",")
        print ("numberlist",numberlist)

        winNumbers.append(int(numberlist[0]))
        winNumbers.append(int(numberlist[1]))
        winNumbers.append(int(numberlist[2]))
        winNumbers.append(int(numberlist[3]))
        winNumbers.append(int(numberlist[4]))
        winNumbers.append(int(numberlist[5].split("+")[0]))
        winNumbers.append(int(numberlist[5].split("+")[1]))

        persons = int(persons)
        total = sum(winNumbers[0:6])

        # 홀수갯수 구하기
        for i in range(0,6):
            if (winNumbers[i] % 2 != 0):
                odd = odd + 1;
        even = 6 - odd  # 짝수갯수는 6 - 홀수갯수

        # bamd 구분하기
        for i in range(0,6):
            if (winNumbers[i] <= 10):
                yellow += 1
            elif (winNumbers[i] >= 11 and winNumbers[i] <= 20):
                blue += 1
            elif (winNumbers[i] >= 21 and winNumbers[i] <= 30):
                red += 1
            elif (winNumbers[i] >= 31 and winNumbers[i] <= 40):
                green += 1
            elif (winNumbers[i] >= 41 and winNumbers[i] <= 45):
                gray += 1
        if (yellow > 0):
            band += 1
        if (blue > 0):
            band += 1
        if (red > 0):
            band += 1
        if (green > 0):
            band += 1
        if (gray > 0):
            band += 1

        #continure number 구하기
        #1 연번
        if (winNumbers[1] - winNumbers[0] == 1):
            one_continue += 1
        elif (winNumbers[2] - winNumbers[1] == 1):
            one_continue += 1
        elif (winNumbers[3] - winNumbers[2] == 1):
            one_continue += 1
        elif (winNumbers[4] - winNumbers[3] == 1):
            one_continue += 1
        elif (winNumbers[5] - winNumbers[4] == 1):
            one_continue += 1

        #2 연번
        if (winNumbers[2] - winNumbers[0] == 2):
            two_continue += 1
            one_continue -= 1
        elif (winNumbers[3] - winNumbers[1] == 2):
            two_continue += 1
            one_continue -= 1
        elif (winNumbers[4] - winNumbers[2] == 2):
            two_continue += 1
            one_continue -= 1
        elif (winNumbers[5] - winNumbers[3] == 2):
            two_continue += 1
            one_continue -= 1

        #3 연번
        if (winNumbers[3] - winNumbers[0] == 3):
            three_continue += 1
            two_continue -= 1
        elif (winNumbers[4] - winNumbers[1] == 3):
            three_continue += 1
            two_continue -= 1
        elif (winNumbers[5] - winNumbers[2] == 3):
            three_continue += 1
            two_continue -= 1

        #4 연번
        if (winNumbers[4] - winNumbers[0] == 4):
            four_continue += 1
            three_continue += 1
        elif (winNumbers[5] - winNumbers[1] == 4):
            four_continue += 1
            three_continue += 1

        #끝자리수 횟수 확인
        ending_digit = []

        for i in range(0,6):
            if (winNumbers[i] <= 9):
                ending_digit.append(winNumbers[i])
            elif (winNumbers[i] >= 10 and winNumbers[i] <= 19):
                ending_digit.append(winNumbers[i] - 10)
            elif (winNumbers[i] >= 20 and winNumbers[i] <= 29):
                ending_digit.append(winNumbers[i] - 20)
            elif (winNumbers[i] >= 30 and winNumbers[i] <= 39):
                ending_digit.append(winNumbers[i] - 30)
            elif (winNumbers[i] >= 40 and winNumbers[i] <= 45):
                ending_digit.append(winNumbers[i] - 40)
        unique_elements, counts_elements = np.unique(ending_digit, return_counts=True)
        max_ending_digit_count = int(max(counts_elements))  # max count

       # if a model has an AutoField but you want to define a new object's ID
        insert_data = nums(id=count,
                          count=count,
                          one = winNumbers[0],
                          two = winNumbers[1],
                          three = winNumbers[2],
                          four = winNumbers[3],
                          five = winNumbers[4],
                          six = winNumbers[5],
                          bonus = winNumbers[6],
                          person = persons,
                          amount = amounts,
                          total = total,
                          odd = odd,
                          even = even,
                          yellow = yellow,
                          blue = blue,
                          red = red,
                          green = green,
                          gray = gray,
                          band = band,
                          one_continue = one_continue,
                          two_continue = two_continue,
                          three_continue = three_continue,
                          four_continue = four_continue,
                          end_digit = max_ending_digit_count)
        insert_data.save()

