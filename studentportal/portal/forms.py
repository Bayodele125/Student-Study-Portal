from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Homework,Notes, Todo
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title','description')

class DateType(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model= Homework
        Widget = {'due':DateType()}
        fields = ['subject','title','desciption','due','is_finished']

class DashboardForm(forms.Form):
    text =forms.CharField(max_length=100, label='Enter  Your Search')

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields =['title','is_finished']

class ConversionForm(forms.Form):
    # TODO: Define form fields here
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [
        ('inch', 'Inch'), ('foot', 'Foot'), ('yard', 'Yard'), ('mile', 'Mile'),
        ('millimeter', 'Millimeter'), ('centimeter', 'Centimeter'),
        ('meter', 'Meter'), ('kilometer', 'Kilometer')
    ]

    inputs = forms.CharField(required=False, label=False, widget=forms.TextInput(
            attrs = {'type':'number', 'placeholder':'Enter the Number'}
        ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionMassForm(forms.Form):
    CHOICES = [
        ('milligram', 'Milligram'), ('gram', 'Gram'),
        ('kilogram', 'Kilogram'), ('ton', 'Metric Ton'),
        ('ounce', 'Ounce'), ('pound', 'Pound'), ('us_ton', 'US Ton')
    ]

    inputs = forms.CharField(required=False, label=False, widget=forms.TextInput(
            attrs = {'type':'number', 'placeholder':'Enter the Number'}
        ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
