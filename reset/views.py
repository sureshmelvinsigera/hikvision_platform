import uuid

import telebot
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render
from field_history.models import FieldHistory

from .forms import ResetTaskListForm
from .models import ResetTaskList


@login_required()
def index(request):
    if request.method == 'POST':
        form = ResetTaskListForm(request.POST, request.FILES)
        if form.is_valid():
            form_files = form.save(commit=False)
            form_files.owner = request.user
            form_files.task_id = str(uuid.uuid4().fields[-1])[:5]
            form_files.save()
            return HttpResponse("Successfully uploaded")
    form = ResetTaskListForm()
    return render(request, 'reset/reset.html', {
        'form': form
    })


bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, parse_mode='HTML')


@receiver(post_save, sender=ResetTaskList)
def add_successfully(sender, instance, **kwargs):
    task = ResetTaskList.objects.get(id=instance.id)
    task_last_version = FieldHistory.objects.filter(field_name='task_status', object_id=instance.id).last()

    if task_last_version is None:  # Новая задача
        for x in settings.TELEGRAM_ADMIN_LIST:
            send_mess(x, f'Новая задача #id{task.task_id} от пользователя #id{task.owner.username}')
        send_mess(task.owner.username, f'Ваша заявка #id{task.task_id} зарегистрирована в системе!')
        return

    if task_last_version.field_value != task.task_status:
        if task.task_status == 'refund':
            send_mess(task.owner.username, f'Ваша заявка #id{task.task_id} была откланена. Для уточнения деталей '
                                           f'свяжитесь с поддержкой!')
        else:
            send_mess(task.owner.username, f'Ваша заявка #id{task.task_id} успешно обработано! '
                                           f'Для получения файла сброса, войдите в кабинет на сайте.')


def send_mess(user_id, message):
    try:
        bot.send_message(
            chat_id=int(user_id),
            text=message
        )
    except telebot.apihelper.ApiTelegramException:
        print('Бот заблокирован')
