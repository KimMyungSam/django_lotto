from django.db import models

from django.utils import timezone
import random
# Create your models here.
class GuessNumbers(models.Model):
    name = models.CharField(max_length = 24)
    lottos = models.CharField(max_length = 255, default = '[1,2,3,4,5,6]')
    text = models.CharField(max_length = 24)
    num_lotto = models.IntegerField(default = 5)
    update_date = models.DateTimeField()

    # 로또 번호 생성 및 데이터베이스 저장
    def generate(self):
        self.lottos = ""
        origin = list(range(1,46))
        for _ in range(0, self.num_lotto):
            random.shuffle(origin)
            guess = origin[:6]
            guess.sort()
            self.lottos += str(guess) +'\n'
        self.update_date = timezone.now()
        self.save()

    def __str__(self):
        return "%s %s" % (self.name, self.text)

class num_history(models.Model):
    count = models.IntegerField(default = 1)
    one = models.IntegerField(default = 1)
    two = models.IntegerField(default = 1)
    three = models.IntegerField(default = 1)
    four = models.IntegerField(default = 1)
    five = models.IntegerField(default = 1)
    six = models.IntegerField(default = 1)
    bonus = models.IntegerField(default = 1)
    person = models.IntegerField(default = 1)
    amount = models.CharField(max_length = 24, default = '1000')
    total = models.IntegerField(default = 1)
    odd = models.IntegerField(default = 1)
    even = models.IntegerField(default = 1)
    yellow = models.IntegerField(default = 1)
    blue = models.IntegerField(default = 1)
    red = models.IntegerField(default = 1)
    green = models.IntegerField(default = 1)
    gray = models.IntegerField(default = 1)
    band = models.IntegerField(default = 1)
    one_continue = models.IntegerField(default = 1)
    two_continue = models.IntegerField(default = 1)
    three_continue = models.IntegerField(default = 1)
    four_continue = models.IntegerField(default = 1)
    end_digit = models.IntegerField(default = 1)

    def __str__(self):
        return "%s %s" % (self.name, self.text)
