from django.db import models

# Users
#     Name
#     Email
#     Password or something (Hash of it?)
#     Sell lists
#     Purchase History
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


# Artist
class Artist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    


# Records
#     List of songs
#     Artist
#     Album Art (tbd)
#     Release Date
#     Length 
#     Edition/Pressing
#     List of genres

class Record(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    #length = models.DurationField()

    @property
    def length(self): # Duration of entire album
        songs = self.song_set.all()
        return sum(song.duration for song in songs)
        

# Songs 
#     Duration
#     Name
#     Artists
class Song(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)

# Listing
#     Price
#     Seller
#     Record
#     Condition
#     Date Posted


