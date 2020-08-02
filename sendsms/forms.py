from django import forms
from .models import *
from sms.views import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count



class SignUpForm(UserCreationForm):
	username = forms.CharField(
				widget=forms.TextInput(
					attrs={
					"class":"input100",
                    "placeholder":"Telephone...",
					
					}
					)
		)

	password1 = forms.CharField(
				widget=forms.TextInput(
					attrs={
					"class":"input100",
                    "placeholder":"Mot de passe...",
					
					}
					)
		)

	password2 = forms.CharField(
				widget=forms.TextInput(
					attrs={
					"class":"input100",
                    "placeholder":"Confirmer mot de passe...",
					
					}
					)
		)
	
	class Meta :
		model = User
		fields = ('username','password1', 'password2',)

		
class VerifForm(forms.ModelForm):
	code_user = forms.CharField(

		widget=forms.TextInput(
			attrs={
			"class":"input100",
            "placeholder":"Code de validation...",
					
					}
		)
	)

	class Meta:
		model = Verif
		fields = [
			'code_user',

		]


class SmsForm(forms.ModelForm):
	address = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Sms
		fields = [
			'address',
			'message',

		]


class RawSmsForm(forms.Form):
	address = forms.CharField(
				
				widget=forms.TextInput(
					attrs={
					
					"class":"tag form-control",
                    "placeholder":"",
					"label": "Numéro"
					
					}
					)
		)

	message = forms.CharField(widget=forms.Textarea(
										attrs={
										"id":"message",
										"class":"form-control space",
                                        "placeholder":"",
										"rows":"4",
										}
		)
		)


class ListeForm(forms.ModelForm):
	nom = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"class":"form-control space",
            "placeholder":"Nom de la liste...",
					
					}
		)
	)
	numeros = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"id":"demo1",
			"class":"form-control compter",
            "placeholder":"Entrer les numéros séparés par une virgule",
					
					}
		)
	)
	

	class Meta:
		model = Liste
		fields=['nom', 'numeros']

class CsvForm(forms.ModelForm):
	groupe = forms.ModelChoiceField(
		queryset=Groupe.objects.values_list('groupe').annotate(dcount=Count('groupe')).all(), 
		widget=forms.Select(
			attrs={
			"class":"form-control space",
            "placeholder":"Nom du groupe...",
					
					}
		)
	)
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={
			"id":"message",
			"class":"form-control space",
            "placeholder":"Votre message...",
			"rows":"4",
					}
		)
	)
	

	class Meta:
		model = Sms
		fields=['groupe', 'message']


class SendlisteForm(forms.ModelForm):
	liste = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"class":"form-control choix",
            "placeholder":"",
					
					}
		)
	)
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={
			"class":"form-control compter",
            "placeholder":"Message...",
			"rows":"4",
					
					}
		)
	)
	

	class Meta:
		model = Sms
		fields=['address', 'message']