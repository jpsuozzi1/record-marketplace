from django import forms
# from django.db import models

class CreateUser(forms.Form):
	first_name = forms.CharField(max_length=50, required=True, label='First Name')
	last_name = forms.CharField(max_length=50, required=True, label='Last Name')
	email = forms.EmailField(required=True)

	# https://docs.djangoproject.com/en/1.10/topics/auth/passwords/
	passwordHash = forms.CharField(max_length=256, required=True, label='Password', widget=forms.PasswordInput())

class LoginUser(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(max_length=100, required=True, label='Password', widget=forms.PasswordInput())

class CreateListing(forms.Form):
	price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
	#seller = forms.CharField(widget=forms.HiddenInput())
	#buyer = forms.ForeignKey(User, related_name='buyer', required=True)
	
	# temporary until search is implemented
	AMEN = 'Amen'
	DARK = 'Dark Side of the Moon'
	PIMP = 'To Pimp a Butterfly'

	NAME_CHOICES = (
		(None, '-------'),
		(AMEN, 'Amen'),
		(DARK, 'Dark Side of the Moon'),
		(PIMP, 'To Pimp A Butterfly'),
	)

	record = forms.ChoiceField(choices=NAME_CHOICES)

	# Condition Options: Mint, Near Mint, Very Good, Good, Fair, Poor
	MINT = 'M'
	NEARMINT = 'NM'
	VERYGOOD = 'VG'
	GOOD = 'G'
	FAIR = 'F'
	POOR = 'P'

	CONDITION_CHOICES = (
		(None, '-------'),
		(MINT, 'Mint'),
		(NEARMINT, 'Near Mint'),
		(VERYGOOD, 'Very Good'),
		(GOOD, 'Good'),
		(FAIR, 'Fair'),
		(POOR, 'Poor')
	)

	condition = forms.ChoiceField(
		choices=CONDITION_CHOICES,
	)

class Search(forms.Form):
	query = forms.CharField(max_length=100, label='Search')
