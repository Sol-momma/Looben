from dataclasses import field
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget

from .models import ReviewOfUniversity
from accounts.models import Schools


class ReviewForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'タイトル',
        'type': 'text',
        }))
    review = forms.CharField(label='レビュー', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '口コミ本文',
        'rows': '8',
        'type': 'textarea',
        }))
    university = forms.ModelChoiceField(label='大学', queryset= Schools.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'レビューを書く大学',
        'type': 'select',
        }))
    star = forms.ChoiceField(label='総合評価', choices=((1, 'とても良くない'), (2, '良くない'), (3, '普通'), (4, '良い'), (5, 'とても良い')), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': '総合評価',
        'type': 'select',
        }))
    
    class Meta:
        model = ReviewOfUniversity
        fields = ['title', 'review', 'university', 'star'] 