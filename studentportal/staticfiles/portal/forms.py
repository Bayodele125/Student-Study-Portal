from django import forms
from .models import *

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search: ")

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass'),('temperature','Temperature'),('volume','Volume'),('area','Area')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('inch','Inch'),('centimeter','Centimeter'),('foot','Foot'),('meter','Meter'),('mile','Mile'),('kilometer','Kilometer'),('yard','Yard'),('millimeter','Millimeter')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram'),('ounce','Ounce'),('gram','Gram'),('ton','Ton'),('milligram','Milligram')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class ConversionTemperatureForm(forms.Form):
    CHOICES = [('celsius','Celsius'),('fahrenheit','Fahrenheit'),('kelvin','Kelvin')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class ConversionVolumeForm(forms.Form):
    CHOICES = [('liter','Liter'),('milliliter','Milliliter'),('gallon','Gallon'),('quart','Quart')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class ConversionAreaForm(forms.Form):
    CHOICES = [('square_meter','Square Meter'),('acre','Acre'),('hectare','Hectare')]
    measurement = forms.ChoiceField(choices = CHOICES, widget= forms.RadioSelect)

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject','title','description','due','is_finished']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
