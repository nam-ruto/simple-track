from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'company',
            'location',
            'job_title',
            'job_url',
            'status',
            'priority',
            'deadline',
            'salary_range',
            'notes',
        ]
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. San Francisco, CA'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. $80,000 - $100,000'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any notes about this application...'}),
        }
