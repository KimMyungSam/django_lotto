from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import generate  # celery.py file imsport

# Create your views here.
from .models import ShootNumbers
from .forms import LottoForm
from .crawling import getLast, checkLast, crawler, insert

def index(request):
    lottos = ShootNumbers.objects.all()
    return render(request, "lotto/default.html", {"lottos": lottos})

def list(request):
    from django.conf import settings
    print (settings.BASE_DIR)

    object_list = ShootNumbers.objects.all()
    paginator = Paginator(object_list, 4) # show per page

    # pagination 처리
    page = request.GET.get('page')
    try:
        lottos = paginator.page(page)
    except PageNotAnInteger:
        # If page is note an interger deliver the first page
        lottos = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        lottos = paginator.page(paginator.num_pages)

    # POST Form 처리
    if request.method == "POST":
        return redirect('index')
    else:
        # lottos = ShootNumbers.objects.all()
        return render(request, "lotto/list.html", {"lottos": lottos})

def post(request):
    if request.method == "POST":
        form = LottoForm(request.POST)
        if form.is_valid():
            lotto = form.save()
            # band별 번호 추출 함수 호출
            generate()  # tasks.py generate()
            return redirect('index')
    else:
        form = LottoForm()
        return render(request, 'lotto/form.html', {"form": form})

def detail(request, lottokey):
    if request.method == "POST":
        return redirect('list_lotto')
    else:
        # lotto = ShootNumbers.objects.get(pk = lottokey)
        lotto = get_object_or_404(ShootNumbers, pk = lottokey)
        return render(request, "lotto/detail.html", {"lotto": lotto})

def crawling(request):
    lotto_list = []
    last_time = getLast()
    dblast_time = checkLast()

    if request.method == "POST":
        return redirect('index')
    else:
        if dblast_time < last_time:
            lotto_list = crawler(dblast_time, last_time)
        #신규 회차 있을때 db update
        if len(lotto_list) > 0:
            insert(lotto_list)
        return render(request, 'lotto/crawling.html',{"last_time":last_time, "dblast_time":dblast_time})
