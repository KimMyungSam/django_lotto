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

class nums(models.Model):
    count = models.IntegerField()
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

    def __str__(self):
        return "%s %s" % (self.name, self.text)
