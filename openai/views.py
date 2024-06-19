import json

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from backend import settings

import urllib3

http = urllib3.PoolManager()


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]


OpenAIChatGPTAPIEndPoint: str = f"https://{settings.OPENAI_DOMAIN}/v1/chat/completions"


class OpenAIChatCompletion(AuthenticatedAPIView):
    def post(self, request):
        params = request.data
        # message: str = params['message']
        # post_json = {
        #     "model": "gpt-3.5-turbo",
        #     "messages": [{"role": "user", "content": message}]
        # }
        if settings.OPENAI_KEY is None:
            raise Exception("OPENAI_KEY is not set.")

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_KEY}",
            "Content-Type": "application/json",
        }
        resp = http.request(
            "POST", OpenAIChatGPTAPIEndPoint,
            headers=headers, body=json.dumps(params).encode("utf-8"))

        ret = {
            "status": resp.status,
            "data": json.loads(resp.data.decode("utf-8")) if resp.status == 200 else None,
        }
        return JsonResponse(ret)
