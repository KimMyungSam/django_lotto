from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
from .models import GuessNumbers
from .forms import PostForm
from .crawling import getLast, checkLast, crawler, insert

def index(request):
    lottos = GuessNumbers.objects.all()
    return render(request, "lotto/default.html", {"lottos": lottos})

def post(request):
    if request.method == "POST":
        # save data
        form = PostForm(request.POST)
        if form.is_valid():
            lotto = form.save(commit = False)
            lotto.generate()
            return redirect('index')
    else:
        form = PostForm()
        return render(request, 'lotto/form.html', {"form": form})

def detail(request, lottokey):
    lotto = GuessNumbers.objects.get(pk = lottokey)
    return render(request, "lotto/detail.html", {"lotto": lotto})

def crawling(request):
    lotto_list = []
    last_time = getLast()
    dblast_time = checkLast()
    if dblast_time == 0:
       dblast_time =1
    # test
    last_time = 2

    if dblast_time < last_time:
        lotto_list = crawler(dblast_time, last_time)

    #신규 회차 있을때 db update
    if len(lotto_list) > 0:
        insert(lotto_list)

    return render(request, 'lotto/crawling.html',{"last_time":last_time, "dblast_time":dblast_time})
