from django import forms

from .models import ResetTaskList


class ResetTaskListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serial_num'].widget.attrs.update({'placeholder': 'Серийный номер'})
        self.fields['sn_images'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['qr_code'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['request_file'].widget.attrs.update({'class': 'custom-file-input'})

    class Meta:
        model = ResetTaskList
        fields = (
            'serial_num',
            'sn_images',
            'qr_code',
            'request_file'
        )
