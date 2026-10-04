from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category

class ReportForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}))
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

class SignUpForm(UserCreationForm):
    pass

class UpdateForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('assigned', 'Assigned'),
                 ('in_progress', 'In Progress'),
                 ('resolved', 'Resolved')],
        widget=forms.Select(attrs={'class': 'form-select'}))
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    proof_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))