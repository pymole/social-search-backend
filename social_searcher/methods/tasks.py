from .lib import helpers
from .lib import vk_requests as vk_r
from collections import defaultdict
from celery import shared_task
from .models import MethodResult


@shared_task
def vk_word_rate(result_id, vk_user_id, token):
    vk_user_id = vk_r.search_user(vk_user_id, token)

    # запрашиваем лист групп
    user_groups = vk_r.get_user_groups(vk_user_id, token)

    if user_groups:
        post_list = vk_r.get_post(user_groups, token, mode='group')
        post_list = [post['text'] for post in post_list]

        result = helpers.word_rate(post_list)

        r = MethodResult.objects.get(pk=result_id)
        r.result = {'method': 'word_rate', 'result': result}
        r.save()


@shared_task
def vk_user_group_city(result_id, vk_user_id, token):
    vk_user_id = vk_r.search_user(vk_user_id, token)

    user_groups = vk_r.get_user_groups(vk_user_id, token, fields=('city',), extended=True)
    if user_groups:
        result = defaultdict(list)

        for g in user_groups:
            city = g.get('city')
            if city:
                result[city['title']].append({
                    'name': g['name'],
                    'screen_name': g['screen_name'],
                    'photo': g['photo_100']
                })

        # for c in result:
        #     print(c, len(result[c]))

        r = MethodResult.objects.get(pk=result_id)
        r.result = {'method': 'user_group_city', 'result': result}
        r.save()
