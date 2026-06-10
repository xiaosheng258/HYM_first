from django import forms
from django.utils import timezone

from .models import Resume


class ResumeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial.setdefault('sex', '男')
            self.initial.setdefault('edu', '本科')
            self.initial.setdefault('birth', timezone.localdate())
        for name, field in self.fields.items():
            if name == 'photo':
                continue
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['experience'].widget.attrs.update({'class': 'form-control', 'rows': 10})

    class Meta:
        model = Resume
        fields = (
            'name',
            'personID',
            'sex',
            'birth',
            'email',
            'edu',
            'school',
            'major',
            'position',
            'photo',
            'experience',
        )
