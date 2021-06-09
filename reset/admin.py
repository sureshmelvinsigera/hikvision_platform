from django.contrib import admin

from reset.models import ResetTaskList


@admin.register(ResetTaskList)
class ResetTaskListAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'task_status', 'serial_num', 'owner', 'upload_at']
    list_display_links = ['task_id', 'serial_num']
    ordering = ['task_status', 'task_id', 'serial_num', 'owner', 'upload_at']
    search_fields = ['task_id', 'serial_num']

    readonly_fields = ['task_id', 'serial_num', 'owner', 'upload_at']

