from . import tasks
from .models import MethodResult


def is_vk_authenticated(request):
    return request.user.is_vk_authorized


def vk_word_rate(request):
    vk_user_id = request.query_params.get('user_id')
    if not vk_user_id:
        return {'error': 'Need user_id'}

    mr = MethodResult.objects.create(user=request.user)
    result = tasks.vk_word_rate.delay(mr.id, vk_user_id, request.user.vk_token)

    mr.task_id = result.id
    mr.save()

    return {'message': 'Word Rate task created'}


def vk_user_group_city(request):
    vk_user_id = request.query_params.get('user_id')
    if not vk_user_id:
        return {'error': 'Need user_id'}

    mr = MethodResult.objects.create(user=request.user)
    result = tasks.vk_user_group_city.delay(mr.id, vk_user_id, request.user.vk_token)

    mr.task_id = result.id
    mr.save()

    return {'message': "User's groups cities task created"}
