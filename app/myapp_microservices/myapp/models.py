from django.db import models
import datetime

# See https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey

# Users
#     Name
#     Email
#     Password Hash
#     Sell lists
#     Purchase History
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    # https://docs.djangoproject.com/en/1.10/topics/auth/passwords/
    passwordHash = models.CharField(max_length=255)

    @property
    def sellList(self):
        return self.seller.all()

    @property
    def purchaseHistory(self):
        return self.buyer.all()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

# Authenticator
#   Each logged on user gets an Authenticator to show they
#   are logged on.
#   Delete once user logs out
#
#
class Authenticator(models.Model):
    user_id = models.IntegerField()
    authenticator = models.CharField(max_length=255, primary_key=True)
    date_created  = models.DateField()

    def __str__(self):
        return 'User id: %i Auth: %s' % (self.user_id, self.authenticator)

# Artist
class Artist(models.Model):
    name = models.CharField(max_length=50)


    @property
    def songList(self):
        return self.song_set.all()

    @property
    def albumList(self):
        return self.record_set.all()

    def __str__(self):
        return '%s' % (self.name)

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
    pressing = models.CharField(max_length=100)

    @property
    def length(self): # Duration of entire album
        songSet = self.song_set.all()
        sum = datetime.timedelta()
        for song in songSet:
            sum += song.duration
        return sum

    @property
    def songLists(self):
        return self.song_set.all()

    def __str__(self):
        return '%s by %s' % (self.name, self.artist)

# Songs
#     Duration
#     Name
#     Artist
#     Record
class Song(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)

    def __str__(self):
        return '\"%s\" by %s' % (self.name, self.artist)

# Listing
#     Price
#     Seller
#     Record
#     Condition
#     Date Posted
class Listing(models.Model):
    price = models.DecimalField(max_digits=6,decimal_places=2)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE, blank=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date_posted = models.DateField()

    # Condition Options: Mint, Near Mint, Very Good, Good, Fair, Poor
    MINT = 'M'
    NEARMINT = 'NM'
    VERYGOOD = 'VG'
    GOOD = 'G'
    FAIR = 'F'
    POOR = 'P'

    CONDITION_CHOICES = (
        (MINT, 'Mint'),
        (NEARMINT, 'Near Mint'),
        (VERYGOOD, 'Very Good'),
        (GOOD, 'Good'),
        (FAIR, 'Fair'),
        (POOR, 'Poor')
    )

    condition = models.CharField(
        max_length=2,
        choices=CONDITION_CHOICES,
        default=POOR,
    )

    def __str__(self):
        return '%s selling %s' % (self.seller, self.record)

# Genre
# Name
# Record
class Genre(models.Model):
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name="genre",
        related_query_name="genre",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.name)
