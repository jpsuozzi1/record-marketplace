from django.forms import ModelForm
from django import forms
from myapp.models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        #fields = ['first_name', 'last_name', 'email', 'passwordHash']
        fields = '__all__'

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        #fields = ['name']
        fields = '__all__'

class RecordForm(ModelForm):
    class Meta:
        model = Record
        #fields = ['artist', 'name', 'release_date', 'pressing']
        fields = '__all__'

class SongForm(ModelForm):
    class Meta:
        model = Song
        #fields = ['name', 'duration', 'artist', 'record']
        fields = '__all__'

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        #fields = ['price', 'seller', 'buyer', 'record', 'date_posted']
        fields = '__all__'

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        #fields = ['record', 'name'] 
        fields = '__all__'
