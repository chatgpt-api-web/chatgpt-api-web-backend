from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class GetLoggedInUserDetailView(APIView):
    permission_classes = []

    def post(self, request):
        if request.user is not None:
            if not request.user.is_anonymous:
                if request.user.is_authenticated:
                    return JsonResponse(
                        {
                            'is_logged_in': True,
                            'username': request.user.username,
                        }
                    )

        return JsonResponse(
            {
                'is_logged_in': False,
                'username': None,
            }
        )


class LoginGetTokenView(APIView):
    permission_classes = []

    def post(self, request):
        params = request.data
        username = params['username']
        password = params['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.update_or_create(user=user)
            return JsonResponse(
                {
                    'username': username,
                    'token': token.key,
                }
            )
        else:
            return JsonResponse(
                {
                    'username': None,
                    'token': None,
                }
            )
