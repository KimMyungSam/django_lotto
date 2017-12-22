from django.shortcuts import render
from .decorators import bot
from . import functions

# Create your views here.
@bot
def on_init(request):
    return {'type':'text'}

@bot
def on_message(request):
    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content']

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

