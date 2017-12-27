import requests
from django.shortcuts import render
from .decorators import bot
from . import functions
from .models import Post
from django.core.files import File
from os.path import basename

# Create your views here.
@bot
def on_init(request):
    return {'type':'text'}

@bot
def on_message(request):
    user_key = request.JSON['user_key']
    type = request.JSON['type']  # text, photo, audio(m4a), video(mp4)
    content = request.JSON['content']  # photo 타입일 경우에는 이미지 url

    #plusfriend/picture diary
    if type == 'photo':
        img_url = content
        img_name = basename(img_url)
        res = requests.get(img_url, stream=True)
        post = Post(user=request.user)
        post.photo.save(img_name, File(res.raw))
        post.save()
        response = "media saved"
    else:
        post = Post.objects.create(user=request.user, message=content)
        response = 'Mr.{} saved your post.'.format(request.user.username)

    # plusfriend/melon search
    if content.startswith('melon:'):
        query = content[6:]
        response = 'melon "{}" result\n\n'.format(query) + functions.melon_search(query)
    else:
        response = "command is not working"

    return {
        'message':{
            'text':response,
        }
    }

@bot
def on_added(request):
    user_key = request.JSON['user_key']

@bot
def on_block(request, user_key):
    pass

@bot
def on_leave(request, user_key):
    pass

def post_list(request, user_key):
    qs = Post.objects.filter(user__username=user_key)
    return render(request, 'plusfriend/post_list.html',{
        'post_list':qs,
    })
