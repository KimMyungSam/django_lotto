from django.shortcuts import render
from .decorators import bot
from . import functions
from .models import Post

# Create your views here.
@bot
def on_init(request):
    return {'type':'text'}

@bot
def on_message(request):
    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content']

    # plusfriend/melon search
    if content.startswith('melon:'):
        query = content[6:]
        response = 'melon "{}" result\n\n'.format(query) + functions.melon_search(query)
    else:
        response = "command is not working"

    #plusfriend/picture diary
    if type == 'photo':
        response = "media is not working"
    else:
        post = Post.objects.create(user=request.user, message=content)
        response = 'Mr.{} saved your post.'.format(request.user.username)

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

