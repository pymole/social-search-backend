from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import config
from .models import MethodResult
from social_searcher.celery import celery_app
# from .tasks import test


class MethodView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        method_result = MethodResult.objects.filter(user=request.user)
        if not method_result:
            return Response({'error': 'No results'})

        method_result = method_result[0]

        if method_result.result is None:
            return Response({'status': 'processing'})

        return Response(method_result.result)

    def post(self, request):
        social = request.query_params.get('social')
        if not social:
            return Response({'error': 'Need social in parameters'})
        if social not in config.METHODS:
            return Response({'error': 'Wrong social'})

        # authentication checks
        auth_handler = config.METHODS[social]['auth_handler']
        if not auth_handler(request):
            return Response({'error': 'No social authentification'})

        method = request.query_params.get('method')
        if not method:
            return Response({'error': 'Need method in parameters'})
        if method not in config.METHODS[social]['methods']:
            return Response({'error': 'Wrong method'})


        # delete all previous results
        method_result = MethodResult.objects.filter(user=request.user)
        if method_result:
            method_result = method_result[0]
            if method_result.result is None:
                celery_app.control.revoke(method_result.task_id, terminate=True)

            method_result.delete()

        handler = config.METHODS[social]['methods'][method]
        result = handler(request)
        return Response(result)
