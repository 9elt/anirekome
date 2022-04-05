from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from anirekome_api.models import Anime, UserList, UserModel
from .functions import getAnime, getUserList, buildUserModel, GetUserRekome
from django.template.loader import render_to_string

import json
with open ('/etc/secret_keys.json') as json_keys:
    secret_keys = json.load(json_keys)

ALPHA_KEY = secret_keys['ALPHA_KEY']

def index(request):
    return render(request, 'index.html')
    
def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')
    
def getRekome(request):

    if('alphakey' not in request.POST or request.POST.get('alphakey') != ALPHA_KEY): 
        response = {'status': 405, 'message' : 'Invalid Access Key'}
        return JsonResponse(response)

    if('user_name' not in request.session): request.session['user_name'] = str(request.POST.get('user')).strip()
    if('ptw' not in request.session): request.session['ptw'] = str(request.POST.get('ptw'))
    user = request.session['user_name']
    if('trashed' in request.session): trashed = request.session['trashed']
    else:trashed = []
    rekomes = GetUserRekome(user, trashed, request.session['ptw'])
    if(isinstance(rekomes, int)):
        del request.session['user_name']
        message = 'error '+str(rekomes)
        if(rekomes == 404): message = 'AnimeList Not Found'
        if(rekomes == 403): message = 'AnimeList Is Private'
        if(rekomes == 500): message = 'You Have No Rekomes'
        response = {'status': rekomes, 'message' : message}
        return JsonResponse(response)
    else:
        if('rekomes' in request.session): del request.session['rekomes']
        request.session['rekomes'] = rekomes
        section = render_to_string('sections/rekome.html', {'rekomes': rekomes})
        nav = render_to_string('sections/nav.html', {'user_name': user})
        response = {'section': section, 'nav': nav, 'status': 200}
        return JsonResponse(response)

def refreshRekome(request):
    
    UserList.objects.filter(pk=request.session['user_name']).delete()
    UserModel.objects.filter(pk=request.session['user_name']).delete()
    return getRekome(request)

def moreRekome(request):

    user = request.session['user_name']
    trashed = request.session['trashed']
    rekomes = GetUserRekome(user, trashed, request.session['ptw'])
    if(rekomes == 500):return  JsonResponse({'status': 500})
    request.session['rekomes'] = rekomes
    request.session.modified = True
    section = render_to_string('sections/rekomore.html', {'rekomes': rekomes})
    response = {'section': section, 'status': 200}
    return JsonResponse(response)   

def trashRekome(request):

    if('trashed' not in request.session): request.session['trashed'] = []
    trash_id = int(request.POST.get('id'))
    for i in range(len(request.session['rekomes'])):
        if(request.session['rekomes'][i]['anime_id'] == trash_id):
            request.session['trashed'].append(request.session['rekomes'][i]['anime_id'])
            request.session['rekomes'].pop(i)
            break
    request.session.modified = True
    return HttpResponse(200)

def disconnectUser(request):

    if('user_name' in request.session): request.session.delete()
    section = render_to_string('sections/connect.html')
    nav = ''
    response = {'section': section, 'nav': nav, 'status': 200}
    return JsonResponse(response)

