from django.contrib.auth.models import User
from django.db import models
from field_history.tracker import FieldHistoryTracker

from config.settings import MEDIA_URL


class ResetTaskList(models.Model):
    """
    Класс для хранения файлов запросов для устройств
    """
    task_id = models.CharField(null=False, max_length=15, verbose_name='ID задачи')
    serial_num = models.CharField(null=False, max_length=50, verbose_name='Сериный номер')
    sn_images = models.ImageField(upload_to='reset/', null=False, verbose_name='Фото серийника')
    qr_code = models.ImageField(upload_to='reset/', null=False, blank=True, verbose_name='QR код')
    request_file = models.FileField(upload_to='reset/', null=False, verbose_name='Файл запроса')
    STATUS = (
        ("processing", "обработка"),
        ("refund", "возврат"),
        ("finish", "обработано"),
    )
    task_status = models.CharField(choices=STATUS, max_length=15, default='processing', verbose_name='Статус запроса')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    field_history = FieldHistoryTracker(['task_status'])

    reset_file = models.FileField(upload_to='reset/', null=True, blank=True, verbose_name='Файл сброса')
    upload_at = models.DateField(auto_now_add=True, verbose_name='Дата создания запроса')

    class Meta:
        verbose_name = 'задача для сброса'
        verbose_name_plural = 'задачи для сброса'

    def __str__(self):
        return self.task_id

    def get_reset_file_url(self):
        print(self.reset_file.url)
        return MEDIA_URL + self.reset_file.url
