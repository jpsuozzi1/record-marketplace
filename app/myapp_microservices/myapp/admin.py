from django.contrib import admin
from .models import User, Artist, Record, Song, Listing, Genre

# Register your models here.

admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Record)
admin.site.register(Song)
admin.site.register(Listing)
admin.site.register(Genre)