from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError

from reset.models import ResetTaskList


@login_required()
def index(request):
    device = ResetTaskList.objects.filter(owner=request.user)
    return render(request, 'user/dash.html', {'device_list': device})


def auth(request):
    if not request.GET.get('hash'):
        return render(request, 'registration/login.html')

    try:
        result = verify_telegram_authentication(bot_token=settings.TELEGRAM_BOT_TOKEN, request_data=request.GET)
        try:
            User.objects.create_user(username=result['id'],
                                     first_name=result.get('first_name', ''),
                                     last_name=result.get('last_name', ''),
                                     password='password')
        except IntegrityError:
            pass
        finally:
            user = authenticate(username=result['id'], password='password')
            login(request, user)
            return redirect('/')

    except TelegramDataIsOutdatedError:
        return render(request, 'alert.html', context={
            'message': {
                'header': 'Ошибка! 😔',
                'content': 'Срок авторизации Телеграм сессии истёк, повторите вход.',
            }
        })

    except NotTelegramDataError:
        return render(request, 'alert.html', context={
            'message': {
                'header': 'Ошибка! 😔',
                'content': 'Ошибка при получении данных из серверов Телеграм, повторите ваш запрос позже.',
            }
        })