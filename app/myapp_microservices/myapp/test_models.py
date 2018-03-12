from django.test import TestCase, Client
import datetime
from myapp.models import User, Artist, Record, Song, Listing, Genre

# Create your tests here.
class UserModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create(first_name='John', last_name='Smith', email='johnsmith@test.com', passwordHash='passwd')
		cls.user2 = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='passwd')
		user1 = cls.user1
		user2 = cls.user2
		cls.artist = Artist.objects.create(name='The Grateful Dead')
		artist = cls.artist
		cls.record = Record.objects.create(name='Terrapin Station', artist=artist, release_date=datetime.date.today(), pressing='test')
		record = cls.record
		cls.listing1 = Listing.objects.create(price=50, seller=user1, buyer=user2, record=record, date_posted=datetime.date.today())
		cls.listing2 = Listing.objects.create(price=75, seller=user2, buyer=user1, record=record, date_posted= datetime.date.today())

	def test_first_name_label(self):
		user = self.user1
		field_label = user._meta.get_field('first_name').verbose_name
		self.assertEquals(field_label, 'first name')

	def test_last_name_label(self):
		user = self.user1
		field_label = user._meta.get_field('last_name').verbose_name
		self.assertEquals(field_label, 'last name')

	def test_email_label(self):
		user = self.user1
		field_label = user._meta.get_field('email').verbose_name
		self.assertEquals(field_label, 'email')

	def test_first_name_max_length(self):
		user = self.user1
		max_length = user._meta.get_field('first_name').max_length
		self.assertEquals(max_length, 50)

	def test_last_name_max_length(self):
		user = self.user1
		max_length = user._meta.get_field('last_name').max_length
		self.assertEquals(max_length, 50)

	def test_password_max_length(self):
		user = self.user1
		max_length = user._meta.get_field('passwordHash').max_length
		self.assertEquals(max_length, 100)

	def test_object_name_is_first_last(self):
		user = self.user1
		expected_object_name = '%s %s' % (user.first_name, user.last_name)
		self.assertEquals(expected_object_name, str(user))

	def test_sell_list(self):
		user = self.user1
		sell_list = user.sellList
		listing = sell_list[0]
		self.assertEquals(len(sell_list), 1)
		self.assertEquals(listing, self.listing1)


	def test_purchase_history(self):
		user = self.user1
		purchase_list = user.purchaseHistory
		listing = purchase_list[0]
		self.assertEquals(len(purchase_list), 1)
		self.assertEquals(listing, self.listing2)


class ArtistModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.artist = Artist.objects.create(name='The Grateful Dead')
		artist = cls.artist
		cls.record = Record.objects.create(name='Terrapin Station', artist=artist, release_date=datetime.date.today(), pressing='test')
		record = cls.record
		d = datetime.timedelta(seconds=225)
		cls.song = Song.objects.create(name='Eyes of the World', artist=artist, record=record, duration=d)

	def test_name_label(self):
		artist = self.artist
		field_label = artist._meta.get_field('name').verbose_name
		self.assertEquals(field_label, 'name')

	def test_name_max_length(self):
		artist = self.artist
		max_length = artist._meta.get_field('name').max_length
		self.assertEquals(max_length, 50)


	def test_object_name(self):
		artist = self.artist
		expected_object_name = '%s' % (artist.name)
		self.assertEquals(expected_object_name, str(artist))

	def test_song_list(self):
		artist = self.artist
		song_list = artist.songList
		song = song_list[0]
		self.assertEquals(len(song_list), 1)
		self.assertEquals(song.id, 1)
		self.assertEquals(song, self.song)

	def test_record_list(self):
		artist = self.artist
		record_list = artist.albumList
		record = record_list[0]
		self.assertEquals(len(record_list), 1)
		self.assertEquals(record.id, 1)
		self.assertEquals(record, self.record)


class RecordModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.artist = Artist.objects.create(name='The Grateful Dead')
		artist = cls.artist
		cls.record = Record.objects.create(name='Terrapin Station', artist=artist, release_date=datetime.date.today(), pressing='test')
		record = cls.record
		d = datetime.timedelta(seconds=225)
		d2 = datetime.timedelta(seconds=255)
		cls.song1 = Song.objects.create(name='Eyes of the World', artist=artist, record=record, duration=d)
		cls.song2 = Song.objects.create(name='Scarlet Begonias', artist=artist, record=record, duration=d2)


	def test_name_label(self):
		record = self.record
		field_label = record._meta.get_field('name').verbose_name
		self.assertEquals(field_label, 'name')

	def test_artist_label(self):
		record = self.record
		field_label = record._meta.get_field('artist').verbose_name
		self.assertEquals(field_label, 'artist')

	def test_release_date_label(self):
		record = self.record
		field_label = record._meta.get_field('release_date').verbose_name
		self.assertEquals(field_label, 'release date')

	def test_pressing_label(self):
		record = self.record
		field_label = record._meta.get_field('pressing').verbose_name
		self.assertEquals(field_label, 'pressing')

	def test_name_max_length(self):
		record = self.record
		max_length = record._meta.get_field('name').max_length
		self.assertEquals(max_length, 100)

	def test_pressing_max_length(self):
		record = self.record
		max_length = record._meta.get_field('pressing').max_length
		self.assertEquals(max_length, 100)


	def test_object_name_is_name_then_artist(self):
		record = self.record
		artist = record.artist
		expected_object_name = '%s by %s' % (record.name, record.artist)
		self.assertEquals(expected_object_name, str(record))

	def test_song_list(self):
		record = self.record
		song_list = record.songLists
		song1 = song_list[0]
		song2 = song_list[1]
		self.assertEquals(len(song_list), 2)
		self.assertEquals(song1, self.song1)
		self.assertEquals(song2, self.song2)

	def test_length(self):
		record = self.record
		song1 = self.song1
		song2 = self.song2
		dur1 = song1.duration
		dur2 = song2.duration
		record_duration = record.length
		self.assertEquals(record_duration, dur1 + dur2)


class SongModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.artist = Artist.objects.create(name='The Grateful Dead')
		artist = cls.artist
		cls.record = Record.objects.create(name='Terrapin Station', artist=artist, release_date=datetime.date.today(), pressing='test')
		record = cls.record
		d = datetime.timedelta(seconds=225)
		cls.song = Song.objects.create(name='Eyes of the World', record=record, duration=d, artist=artist)

	def test_name_label(self):
		song = self.song
		field_label = song._meta.get_field('name').verbose_name
		self.assertEquals(field_label, 'name')

	def test_artist_label(self):
		song = self.song
		field_label = song._meta.get_field('artist').verbose_name
		self.assertEquals(field_label, 'artist')

	def test_record_label(self):
		song = self.song
		field_label = song._meta.get_field('record').verbose_name
		self.assertEquals(field_label, 'record')

	def test_duration_label(self):
		song = self.song
		field_label = song._meta.get_field('duration').verbose_name
		self.assertEquals(field_label, 'duration')

	def test_name_max_length(self):
		song = self.song
		max_length = song._meta.get_field('name').max_length
		self.assertEquals(max_length, 100)

	def test_object_name_is_name_then_artist(self):
		song = self.song
		artist = song.artist
		expected_object_name = '\"%s\" by %s' % (song.name, artist)
		self.assertEquals(expected_object_name, str(song))


class ListingModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create(first_name='John', last_name='Smith', email='johnsmith@test.com', passwordHash='passwd')
		cls.user2 = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='passwd')
		user1 = cls.user1
		user2 = cls.user2
		cls.artist = Artist.objects.create(name='The Grateful Dead')
		artist = cls.artist
		cls.record = Record.objects.create(name='Terrapin Station', artist=artist, release_date=datetime.date.today(), pressing='test')
		record = cls.record
		cls.listing = Listing.objects.create(price=50, seller=user1, buyer=user2, record=record, date_posted=datetime.date.today(), condition='NM')

	def test_price_label(self):
		listing = self.listing
		field_label = listing._meta.get_field('price').verbose_name
		self.assertEquals(field_label, 'price')

	def test_seller_label(self):
		listing = self.listing
		field_label = listing._meta.get_field('seller').verbose_name
		self.assertEquals(field_label, 'seller')

	def test_buyer_label(self):
		listing = self.listing
		field_label = listing._meta.get_field('buyer').verbose_name
		self.assertEquals(field_label, 'buyer')

	def test_record_label(self):
		listing = self.listing
		field_label = listing._meta.get_field('record').verbose_name
		self.assertEquals(field_label, 'record')

	def test_date_posted_label(self):
		listing = self.listing
		field_label = listing._meta.get_field('date_posted').verbose_name
		self.assertEquals(field_label, 'date posted')

	def test_price_max_digits(self):
		listing = self.listing
		max_digits = listing._meta.get_field('price').max_digits
		decimal_places = listing._meta.get_field('price').decimal_places
		self.assertEquals(decimal_places, 2)

	def test_object_name_is_seller_then_record(self):
		listing = self.listing
		seller = listing.seller
		record = listing.record
		expected_object_name = '%s selling %s' % (seller, record)
		self.assertEquals(expected_object_name, str(listing))
