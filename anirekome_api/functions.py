from anirekome_api.models import Anime, UserList, UserModel
from time import sleep
import requests

import json
with open ('/etc/secret_keys.json') as json_keys:
    secret_keys = json.load(json_keys)

CLIENT_ID = secret_keys['CLIENT_ID']

def getAnime(id):
    mal_response = requests.get('https://api.myanimelist.net/v2/anime/'+ str(id) +'?fields=id,title,main_picture,start_date,mean,status,genres,num_episodes,rating,related_anime',headers={'X-MAL-CLIENT-ID': CLIENT_ID})
    if(mal_response.status_code == 200):
        anime_details = mal_response.json()

        if('main_picture' in anime_details):
            if('large' in anime_details['main_picture']):
                anime_details['main_picture'] = anime_details['main_picture']['large']
            elif('medium' in anime_details['main_picture']):
                anime_details['main_picture'] = anime_details['main_picture']['medium']
        else:anime_details['main_picture'] = ''
        
        if('start_date' in anime_details):
            raw_date = int(anime_details['start_date'][0:4])
            if(0 < raw_date <= 1990):anime_details['start_date'] = '80s'
            elif(1990 < raw_date <= 1999):anime_details['start_date'] = '90s'
            elif(1999 < raw_date <= 2009):anime_details['start_date'] = '00s'
            elif(2009 < raw_date <= 2015):anime_details['start_date'] = '10s'
            elif(2015 < raw_date <= 2020):anime_details['start_date'] = '20s'
            else:anime_details['start_date'] = ''
        else:anime_details['start_date'] = ''

        if('num_episodes' in anime_details):
            if(anime_details['num_episodes'] == 1):anime_details['num_episodes'] = '1ep'
            elif(1 < anime_details['num_episodes'] <= 8):anime_details['num_episodes'] = '6ep'
            elif(8 < anime_details['num_episodes'] <= 18):anime_details['num_episodes'] = '12ep'
            elif(18 < anime_details['num_episodes'] <= 32):anime_details['num_episodes'] = '24ep'
            elif(anime_details['num_episodes'] > 32):anime_details['num_episodes'] = '48ep'
            else:anime_details['num_episodes'] = ''
        else:anime_details['num_episodes'] = ''

        if('status' in anime_details):pass
        else:anime_details['status'] = ''

        if('rating' in anime_details):
            if(anime_details['rating'] == 'rx'):pass
            elif(anime_details['rating'] == 'r+'):pass
            elif(anime_details['rating'] == 'r'):pass
            elif(anime_details['rating'] == 'pg_13'):pass
            elif(anime_details['rating'] == 'g'):pass
            elif(anime_details['rating'] == 'pg'):pass
            else:anime_details['rating'] = ''
        else:anime_details['rating'] = ''

        if('genres' in anime_details):
            genres = []
            for gnr in range(len(anime_details['genres'])):
                genres.append(anime_details['genres'][gnr]['name'])
        else: genres = ['',]

        if('related_anime' in anime_details):
            related = []
            for rel in range(len(anime_details['related_anime'])):
                related_anime = {anime_details['related_anime'][rel]['node']['id'] : anime_details['related_anime'][rel]['relation_type']}
                related.append(related_anime)
        else: related = ['',]

        new_anime = Anime(
        anime_id = anime_details['id'], anime_title = anime_details['title'], anime_picture = anime_details['main_picture'], anime_date = anime_details['start_date'],
        anime_mean = anime_details['mean'], anime_status = anime_details['status'], anime_rating = anime_details['rating'], anime_episodes = anime_details['num_episodes'],
        anime_genres = genres, anime_related = related)
        
        new_anime.save()
        return mal_response.status_code
    else:return mal_response.status_code

def getUserList(user):
    user = user.lower()
    mal_list = []
    list_length = 0
    for i in range(35):
        if(list_length == i*1000):
            sleep(1.5)
            mal_response = requests.get('https://api.myanimelist.net/v2/users/'+user+'/animelist?fields=list_status&sort=list_updated_at&limit=1000&nsfw=1&offset='+str(i)+'000', headers={'X-MAL-CLIENT-ID': CLIENT_ID})
            if(mal_response.status_code == 200):
                animelist_response = mal_response.json()
                mal_list.extend(animelist_response["data"])
                list_length = len(mal_list)
        else: break

    if(mal_response.status_code == 200):
        if(list_length == 0): return 500
        new_user_list = UserList(user_name = user, user_list = mal_list)
        new_user_list.save()
        return mal_response.status_code
    else:return mal_response.status_code

def buildUserModel(user):
    user = user.lower()

    if(UserList.objects.filter(pk=user).exists()):pass
    else: 
        list_response = getUserList(user)
        if(list_response == 200):pass
        else: return list_response

    user_list = UserList.objects.get(pk=user)
    user_list = user_list.user_list

    list_length = len(user_list)

    user_model = {
    'start_date' : {'80s' : [0,0,0], '90s' : [0,0,0], '00s' : [0,0,0], '10s' : [0,0,0], '20s' : [0,0,0]},
    'num_episodes' : {'1ep' : [0,0,0], '6ep' : [0,0,0], '12ep' : [0,0,0], '24ep' : [0,0,0], '48ep' : [0,0,0]},
    'rating' : {'rx' : [0,0,0], 'r+' : [0,0,0], 'r' : [0,0,0], 'pg_13' : [0,0,0], 'g' : [0,0,0], 'pg' : [0,0,0]},
    'genres' : {
        'Action' : [0,0,0], 'Adventure' : [0,0,0], 'Fantasy' : [0,0,0], 'Comedy' : [0,0,0], 'Avant Garde' : [0,0,0], 'Mystery' : [0,0,0], 'Drama' : [0,0,0], 'Ecchi' : [0,0,0], 'Hentai' : [0,0,0],
        'Horror' : [0,0,0], 'Romance' : [0,0,0], 'Sci-Fi' : [0,0,0],'Girls Love' : [0,0,0], 'Boys Love' : [0,0,0], 'Sports' : [0,0,0], 'Slice of Life' : [0,0,0], 'Supernatural' : [0,0,0],
        'Suspense' : [0,0,0], 'Gourmet' : [0,0,0], 'Erotica' : [0,0,0]
        },
    'themes' : {
        'Cars' : [0,0,0], 'Demons' : [0,0,0], 'Game' : [0,0,0], 'Historical' : [0,0,0], 'Martial Arts' : [0,0,0], 'Mecha' : [0,0,0], 'Music' : [0,0,0], 'Parody' : [0,0,0], 'Samurai' : [0,0,0],
        'School' : [0,0,0], 'Space' : [0,0,0], 'Super Power' : [0,0,0], 'Vampire' : [0,0,0], 'Harem' : [0,0,0], 'Military' : [0,0,0], 'Police' : [0,0,0], 'Psychological' : [0,0,0]
        },
    'demographics' : {'Shounen' : [0,0,0], 'Shoujo' : [0,0,0], 'Seinen' : [0,0,0], 'Josei' : [0,0,0], 'Kids' : [0,0,0]}
    }

    for i in range(list_length):

        anime_stats = {'id' : 0, 'status' : '', 'score' : 0, 'mean' : 0, 'start_date' : '', 'num_episodes' : '', 'rating' : '', 'genres' : []}

        anime_stats['id'] = user_list[i]['node']["id"]
        for stat in anime_stats:
            if(stat in user_list[i]['list_status']):
                anime_stats[stat] = user_list[i]['list_status'][stat]

        if(Anime.objects.filter(pk=anime_stats['id']).exists()):pass
        else: 
            anime_response = getAnime(anime_stats['id'])
            if(anime_response == 200):pass
            else: continue

        anime_details = Anime.objects.get(pk=anime_stats['id'])

        anime_stats['mean'] = anime_details.anime_mean
        anime_stats['start_date'] = anime_details.anime_date
        anime_stats['num_episodes'] = anime_details.anime_episodes
        anime_stats['rating'] = anime_details.anime_rating
        anime_stats['genres'] = anime_details.anime_genres

        watch_point = 0
        mean_point = 0
        dev_point = 0
 
        if(anime_stats['mean'] > 0 and anime_stats['status'] != 'plan_to_watch'): 
            watch_point = 1
            mean_point = anime_stats['mean']

            if(anime_stats['score'] > 0):
                dev_point = anime_stats['score'] - anime_stats['mean']
            else:dev_point = 0

            if(anime_stats['score'] == 0 and anime_stats['status'] == 'dropped'):
                watch_point = 0
                mean_point = 0
    
        # populating user_model dict
        for cat in anime_stats.keys():
            if(cat == 'genres'):
                for genre in anime_stats['genres']:
                    if(genre in user_model['genres']):
                        user_model['genres'][genre][0] += watch_point
                        user_model['genres'][genre][1] += mean_point
                        user_model['genres'][genre][2] += dev_point
                    elif(genre in user_model['themes']):
                        user_model['themes'][genre][0] += watch_point
                        user_model['themes'][genre][1] += mean_point
                        user_model['themes'][genre][2] += dev_point
                    elif(genre in user_model['demographics']):
                        user_model['demographics'][genre][0] += watch_point
                        user_model['demographics'][genre][1] += mean_point
                        user_model['demographics'][genre][2] += dev_point
            elif(anime_stats[cat] in user_model or
                anime_stats[cat] in user_model['start_date'] or
                anime_stats[cat] in user_model['rating'] or
                anime_stats[cat] in user_model['num_episodes']):
                user_model[cat][anime_stats[cat]][0] += watch_point
                user_model[cat][anime_stats[cat]][1] += mean_point
                user_model[cat][anime_stats[cat]][2] += dev_point

    # calculating percentage of watch model and averaging score and score deviation
    for cat in user_model:
        total_cat_points = 0
    
        for stat in user_model[cat]:
            total_cat_points += user_model[cat][stat][0]
            if(user_model[cat][stat][0] != 0):
                user_model[cat][stat][1] /= user_model[cat][stat][0]
                user_model[cat][stat][2] /= user_model[cat][stat][0]
            else:
                user_model[cat][stat][1] = 0
                user_model[cat][stat][2] = 0
            user_model[cat][stat][1] = (int(user_model[cat][stat][1]*100))/100
            user_model[cat][stat][2] = (int(user_model[cat][stat][2]*100))/100

        for stat in user_model[cat]:
            if(total_cat_points != 0):
                user_model[cat][stat][0] /= total_cat_points
            else:
                user_model[cat][stat][0] = 0

            user_model[cat][stat][0] = int(user_model[cat][stat][0]*100)

    new_user_model = UserModel(
        user_name = user,
        fav_dates = user_model['start_date'], fav_episodes = user_model['num_episodes'], fav_ratings = user_model['rating'],
        fav_genres = user_model['genres'], fav_themes = user_model['themes'], fav_demographics = user_model['demographics']
        )

    new_user_model.save()

    return 200

def GetUserRekome(user, trashed, plantowatch):
    user = user.lower()

    ptw = plantowatch

    if(UserModel.objects.filter(pk=user).exists()):pass
    else: 
        user_model_response = buildUserModel(user)
        if(user_model_response == 200):pass
        else: return user_model_response

    user_model = UserModel.objects.get(pk=user)

    user_model = {
    'start_date' : user_model.fav_dates,
    'num_episodes' : user_model.fav_episodes,
    'rating' : user_model.fav_ratings,
    'genres' : user_model.fav_genres,
    'themes' : user_model.fav_themes,
    'demographics' : user_model.fav_demographics
    }

    from .avg_model import avg_model

    banned_categories = []
    for cat in user_model:
        for stat in user_model[cat]:
            if((user_model[cat][stat][0] - avg_model[cat][stat][0]) < -5 or user_model[cat][stat][0] == 0):
                banned_categories.append(str(stat))

    del avg_model
    user_list = UserList.objects.get(pk=user)
    user_list = user_list.user_list

    this_user_anime = []
    this_user_dropped = []

    this_user_anime.extend(trashed)
    this_user_dropped.extend(trashed)

    for i in range(len(user_list)):
        if(user_list[i]['list_status']['status'] == 'plan_to_watch' and ptw == '1'):
            continue
        this_user_anime.append(user_list[i]['node']['id'])
        if(user_list[i]['list_status']['status'] == 'dropped'):
            this_user_dropped.append(user_list[i]['node']['id'])    

    del user_list

    def getRecommendedUsers(user_model):
        genres_query = {}

        for cat in user_model:
            for stat in user_model[cat]:
                
                if(cat == 'start_date'):sql_cat = 'fav_dates'
                elif(cat == 'num_episodes'):sql_cat = 'fav_episodes'
                elif(cat == 'rating'):sql_cat = 'fav_ratings'
                elif(cat == 'genres'):sql_cat = 'fav_genres'
                elif(cat == 'themes'):sql_cat = 'fav_themes'
                elif(cat == 'demographics'):sql_cat = 'fav_demographics'
                else:continue

                sql_stat = str(stat)

                if(user_model[cat][stat][0] > 4):
                    sql_field_1_gt = (f'{sql_cat}__{sql_stat}__1__gte')
                    sql_field_1_lw = (f'{sql_cat}__{sql_stat}__1__lte')
                    sql_field_2_gt = (f'{sql_cat}__{sql_stat}__2__gte')
                    sql_field_2_lw = (f'{sql_cat}__{sql_stat}__2__lte')
                    genres_query[sql_field_1_gt] = user_model[cat][stat][1] - 1
                    genres_query[sql_field_1_lw] = user_model[cat][stat][1] + 0.5
                    genres_query[sql_field_2_gt] = user_model[cat][stat][2] - 0.6
                    genres_query[sql_field_2_lw] = user_model[cat][stat][2] + 0.6

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 15
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 15


                elif(user_model[cat][stat][0] >= 4):

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 4
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 4

        reko_users = UserModel.objects.filter(**genres_query).values('user_name')
        recommended_users = []
        for user in reko_users:
            recommended_users.append(user['user_name'])
        del reko_users
        return recommended_users

    def getRecommendedUsers2(user_model):
        genres_query = {}

        for cat in user_model:
            for stat in user_model[cat]:
                
                if(cat == 'start_date'):sql_cat = 'fav_dates'
                elif(cat == 'num_episodes'):sql_cat = 'fav_episodes'
                elif(cat == 'rating'):sql_cat = 'fav_ratings'
                elif(cat == 'genres'):sql_cat = 'fav_genres'
                elif(cat == 'themes'):sql_cat = 'fav_themes'
                elif(cat == 'demographics'):sql_cat = 'fav_demographics'
                else:continue

                sql_stat = str(stat)

                if(user_model[cat][stat][0] > 4):
                    sql_field_1_gt = (f'{sql_cat}__{sql_stat}__1__gte')
                    sql_field_1_lw = (f'{sql_cat}__{sql_stat}__1__lte')
                    sql_field_2_gt = (f'{sql_cat}__{sql_stat}__2__gte')
                    sql_field_2_lw = (f'{sql_cat}__{sql_stat}__2__lte')
                    genres_query[sql_field_1_gt] = user_model[cat][stat][1] - 1
                    genres_query[sql_field_1_lw] = user_model[cat][stat][1] + 0.5
                    genres_query[sql_field_2_gt] = user_model[cat][stat][2] - 1
                    genres_query[sql_field_2_lw] = user_model[cat][stat][2] + 1

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 20
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 20


                elif(user_model[cat][stat][0] >= 4):

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 6
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 6

        reko_users = UserModel.objects.filter(**genres_query).values('user_name')
        recommended_users = []
        for user in reko_users:
            recommended_users.append(user['user_name'])
        del reko_users
        return recommended_users 

    def getRecommendedUsers3(user_model):
        genres_query = {}

        for cat in user_model:
            for stat in user_model[cat]:
                
                if(cat == 'start_date'):sql_cat = 'fav_dates'
                elif(cat == 'num_episodes'):sql_cat = 'fav_episodes'
                elif(cat == 'rating'):sql_cat = 'fav_ratings'
                elif(cat == 'genres'):sql_cat = 'fav_genres'
                elif(cat == 'themes'):sql_cat = 'fav_themes'
                elif(cat == 'demographics'):sql_cat = 'fav_demographics'
                else:continue

                sql_stat = str(stat)

                if(user_model[cat][stat][0] > 4):
                    sql_field_1_gt = (f'{sql_cat}__{sql_stat}__1__gte')
                    sql_field_1_lw = (f'{sql_cat}__{sql_stat}__1__lte')
                    sql_field_2_gt = (f'{sql_cat}__{sql_stat}__2__gte')
                    sql_field_2_lw = (f'{sql_cat}__{sql_stat}__2__lte')
                    genres_query[sql_field_1_gt] = user_model[cat][stat][1] - 1
                    genres_query[sql_field_1_lw] = user_model[cat][stat][1] + 0.5
                    genres_query[sql_field_2_gt] = user_model[cat][stat][2] - 1.7
                    genres_query[sql_field_2_lw] = user_model[cat][stat][2] + 1.7

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 25
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 25


                elif(user_model[cat][stat][0] >= 4):

                    sql_field_0_gt = (f'{sql_cat}__{sql_stat}__0__gte')
                    sql_field_0_lw = (f'{sql_cat}__{sql_stat}__0__lte')
                    genres_query[sql_field_0_gt] = user_model[cat][stat][0] - 10
                    genres_query[sql_field_0_lw] = user_model[cat][stat][0] + 10

        reko_users = UserModel.objects.filter(**genres_query).values('user_name')
        recommended_users = []
        for user in reko_users:
            recommended_users.append(user['user_name'])
        del reko_users
        return recommended_users 

    def getRekomesFromUsers(recommended_users):
        ani_rekomes = []
        for reko_user in recommended_users:
            if(reko_user == user):continue
            if(len(ani_rekomes) == 20): break
            reko_list = UserList.objects.get(pk=reko_user)
            reko_list = reko_list.user_list

            for i in range(len(reko_list)):
                rekome_ok = True

                if(reko_list[i]['list_status']['status'] == 'plan_to_watch'): continue
                if(reko_list[i]['list_status']['status'] == 'dropped'): continue
                if(reko_list[i]['list_status']['status'] == 'on_hold'): continue
                if(reko_list[i]['node']['id'] in this_user_anime): continue
                if(0 < reko_list[i]['list_status']['score'] < 6): continue

                anime_details = Anime.objects.get(pk=reko_list[i]['node']['id'])
                if(anime_details.anime_date in banned_categories): rekome_ok = False
                if(anime_details.anime_episodes in banned_categories): rekome_ok = False
                if(anime_details.anime_rating in banned_categories): rekome_ok = False
                for genre in anime_details.anime_genres:
                    if(genre in banned_categories): rekome_ok = False

                for i in range(len(anime_details.anime_related)):
                    if(anime_details.anime_related[i] == 'prequel'):rekome_ok = False
                    if(anime_details.anime_related[i] == 'parent_story'):rekome_ok = False 
                    if(anime_details.anime_related[i].keys in this_user_dropped):rekome_ok = False
                    if(anime_details.anime_related[i].keys in this_user_anime):pass
                    else:rekome_ok = False
                
                if(rekome_ok == False):continue

                expected_score = reko_list[i]['list_status']['score']
                if(expected_score == 0):expected_score = 'ND'

                ani_rekome = {  'anime_id': anime_details.anime_id,
                                'anime_title': anime_details.anime_title,
                                'anime_picture':anime_details.anime_picture,
                                'genres':anime_details.anime_genres,
                                'score':expected_score     }

                this_user_anime.append(anime_details.anime_id)
                ani_rekomes.append(ani_rekome)
                if(len(ani_rekomes) == 20): break

            return ani_rekomes

    recommended_users = getRecommendedUsers(user_model)
    ani_rekomes = getRekomesFromUsers(recommended_users)
    if(ani_rekomes is None): ani_rekomes = []

    if(len(ani_rekomes) < 15):
        recommended_users = getRecommendedUsers2(user_model)
        ani_rekomes = getRekomesFromUsers(recommended_users)
        if(ani_rekomes is None): ani_rekomes = []        

    if(len(ani_rekomes) < 15):
        recommended_users = getRecommendedUsers3(user_model)
        ani_rekomes = getRekomesFromUsers(recommended_users)
        if(ani_rekomes is None): ani_rekomes = []  

    if(len(ani_rekomes) == 0):
        return 500

    return ani_rekomes
