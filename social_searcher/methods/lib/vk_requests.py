# -*- coding: utf-8 -*-

import requests

from django.conf import settings


DEFAULT_PARAMS = {
    'v': settings.VK_VERSION,
}


def request(url, params):
    response = requests.get(url, params=params).json()
    if 'error' in response:
        raise Exception(response)
    return response


def get_user_groups(user_id, token, fields=None, extended=False):
    """Функция для получения групп пользователя.
        Принимается числовой ID пользователя.
        Возвращается список ID групп пользователя.
    """

    params = dict(DEFAULT_PARAMS)
    params.update({
        'user_id': user_id,
        'extended': int(extended),
        'access_token': token,
    })

    if fields:
        params['fields'] = ','.join(fields)

    response = request("https://api.vk.com/method/groups.get", params)
    return response['response']['items']


def get_user_friends(user_id, token):
    params = dict(DEFAULT_PARAMS)
    params.update({
        'user_id': user_id,
        'access_token': token
    })

    response = request("https://api.vk.com/method/friends.get", params)
    return response['response']['items']


def get_post(ids, token, mode='user'):
    """Функция для получения постов группы или пользователя в зависимости от режима (mode).
        Параметры:
            :ids: Список или одиночный ID пользователей или групп.;
            :mode: Режим 'group' или 'users'. По умолчанию 'user'.
    """

    if type(ids) is not list:
        ids = [ids]

    ids = map(str, ids)
    ids = [i if i.isdigit() else get_id(i, mode=mode) for i in ids]

    list_posts = []
    count = 50
    if mode == "group":
        ids = ['-'+i for i in ids]
        count = 100

    params = dict(DEFAULT_PARAMS)
    params.update({
        'owner_id': 0,
        'count': count,
        'access_token': token
    })

    for i in ids:
        params['owner_id'] = i
        try:
            response = request("https://api.vk.com/method/wall.get", params)
            if "error" in response:
                continue

            list_posts += response['response']['items']
        except:
            pass

    return list_posts


def get_id(ids, token, mode='user'):
    """Функция для получения цифрового ID пользователя или группы.
    Принимаемые параметры:
        :ids: короткое имя пользователя или группы
        :mode: для чего искать ID: пользователя или группы ('user', 'group').
        По умолчанию поиск осуществляется для 'user'.
    """
    if type(ids) is not list:
        ids = [ids]

    params = dict(DEFAULT_PARAMS)
    params['access_token'] = token

    if mode == 'user':
        params['user_ids'] = ids
        response = request("https://api.vk.com/method/users.get", params)
        return response['response'][0]['id']
    elif mode == 'group':
        params['group_ids'] = ids
        response = request("https://api.vk.com/method/groups.getById", params)
        return '-' + str(response['response'][0]['id'])


def get_user_info(user_id, token, fields=('city',)):
    """Функция для получения информации о пользователе.
    Принимаемые параметры:
        :user_id: индификатор пользователя (числовой или короткое имя);
        :fields: параметры, которые необходимо получить (Передвать кортеж!). По умолчанию только 'city'.
    Возвращает json-структуру со значениями переданных параметров.
    Пример:
        :запрос: getUserInfo('parametist', ('city', 'home_town'));
        :ответ: {'city': {'id': 147, 'title': 'Тюмень'}, 'home_town': 'Тюмень'}.
    """

    fields = ','.join(fields)

    params = dict(DEFAULT_PARAMS)
    params.update({
        'user_ids': user_id, 'fields': fields,
        'access_token': token
    })

    response = request("https://api.vk.com/method/users.get", params)
    response = response['response'][0]
    response = {k: v for k, v in response.items() if k in fields}

    return response


def get_post_likes(ids, token, post_id):
    """Функция для получения лайков поста.
        Принимает:
            :ids: числовой ID группы или пользователя;
            :post_id: числовой ID поста.
        Возвращает список лайкнувших.
    """

    params = dict(DEFAULT_PARAMS)
    params.update({
        'type': 'post', 'owner_id': ids, 'item_id': post_id,
        'filter': 'likes', 'friends_only': 0, 'extended': 1,
        'offset': 0, 'count': 200, 'skip_own': 0,
        'access_token': token
    })
    response = request('https://api.vk.com/method/likes.getList', params)['response']

    return response


# Поиск цифрового ID
def search_user(user_id, token):
    if not user_id.isdigit():
        user_id = get_id(user_id, token)

    return user_id
