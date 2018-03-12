from django.test import TestCase, Client, TransactionTestCase
import datetime
from myapp.models import User, Artist, Record, Song, Listing

class CreateTestCases(TransactionTestCase):
	def test_create_user(self):
		self.assertEquals(User.objects.all().exists(), False) # DB currently empty
		response = self.client.post('/api/v1/users/create/', {'first_name':'John', 'last_name':'Smith', 'email':'johnsmith@test.com', 'passwordHash':'pass'})
		self.assertEquals(User.objects.all().exists(), True) # DB now has object
		self.assertContains(response, 'John')

	def test_create_artist(self):
		self.assertEquals(Artist.objects.all().exists(), False) # DB currently empty
		response = self.client.post('/api/v1/artists/create/', {'name':'Jerry Garcia'})
		self.assertEquals(Artist.objects.all().exists(), True) # DB now has object
		self.assertContains(response, 'Jerry')

	def test_create_record(self):
		a = Artist.objects.create(name='The Grateful Dead')
		self.assertEquals(Record.objects.all().exists(), False) # DB currently empty
		response = self.client.post('/api/v1/records/create/', {'name':'Terrapin Station', 'artist':a.id, 'release_date':datetime.date.today(), 'pressing':'test'})
		self.assertEquals(Record.objects.all().exists(), True) # DB now has object
		self.assertContains(response, 'Terrapin')

	def test_create_song(self):
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		self.assertEquals(Song.objects.all().exists(), False) # DB currently empty
		response = self.client.post('/api/v1/songs/create/', {'name':'Scarlet Begonias', 'duration':'00:03:45', 'artist':a.id, 'record':r.id})
		self.assertEquals(Song.objects.all().exists(), True) # DB now has object
		self.assertContains(response, 'Scarlet')

	def test_create_listing(self):
		seller = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='pass2')
		buyer = User.objects.create(first_name='Kate', last_name='Shea', email='kateshea@test.com', passwordHash='pass3')
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		self.assertEquals(Listing.objects.all().exists(), False) # DB currently empty
		response = self.client.post('/api/v1/listings/create/', {'price':60, 'seller':seller.id, 'buyer':buyer.id, 'record':r.id, 'date_posted':datetime.date.today()})
		self.assertEquals(Listing.objects.all().exists(), True) # DB now has object
		self.assertContains(response, 60)


class ReadTestCases(TransactionTestCase):
	def test_read_user(self):
		self.assertEquals(User.objects.all().exists(), False) # DB currently empty
		User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='pass2')
		response = self.client.get('/api/v1/users/1/')
		self.assertContains(response, 'Jane')
		self.assertContains(response, 'Doe')
		self.assertContains(response, 'janedoe@test.com')
		self.assertContains(response, 'pass2')

	def test_read_artist(self):
		self.assertEquals(Artist.objects.all().exists(), False) # DB currently empty
		Artist.objects.create(name='The Grateful Dead')
		response = self.client.get('/api/v1/artists/1/')
		self.assertContains(response, 'Dead')

	def test_read_record(self):
		self.assertEquals(Record.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		response = self.client.get('/api/v1/records/1/')
		self.assertContains(response, 'Terrapin')

	def test_read_song(self):
		self.assertEquals(Song.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Song.objects.create(name='Brown Eyed Woman', duration=datetime.timedelta(seconds=287), artist=a, record=r)
		response = self.client.get('/api/v1/songs/1/')
		self.assertContains(response, 'Brown')

	def test_read_listing(self):
		self.assertEquals(Listing.objects.all().exists(), False) # DB currently empty
		seller = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='pass2')
		buyer = User.objects.create(first_name='Kate', last_name='Shea', email='kateshea@test.com', passwordHash='pass3')
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Listing.objects.create(price=55, seller=seller, buyer=buyer, record=r, date_posted=datetime.date.today())
		response = self.client.get('/api/v1/listings/1/')
		self.assertContains(response, 55)
		

class UpdateTestCases(TransactionTestCase):
	def test_update_user(self):
		self.assertEquals(User.objects.all().exists(), False) # DB currently empty
		User.objects.create(first_name='Kate', last_name='Shea', email='kateshea@test.com', passwordHash='pass3')
		response = self.client.post('/api/v1/users/1/update/', {'first_name':'Jess'})
		user = User.objects.get(id=1)
		self.assertContains(response, 'Jess')
		self.assertEquals(user.first_name, 'Jess')

	def test_update_artist(self):
		self.assertEquals(Artist.objects.all().exists(), False) # DB currently empty
		Artist.objects.create(name='The Grateful Dead')
		response = self.client.post('/api/v1/artists/1/update/', {'name':'The Dead'})
		artist = Artist.objects.get(id=1)
		self.assertNotContains(response, 'Grateful')
		self.assertEquals(artist.name, 'The Dead')

	def test_update_record(self):
		self.assertEquals(Record.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		response = self.client.post('/api/v1/records/1/update/', {'pressing':'new pressing'})
		record = Record.objects.get(id=1)
		self.assertContains(response, 'new')
		self.assertEquals(record.pressing, 'new pressing')

	def test_update_song(self):
		self.assertEquals(Song.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Song.objects.create(name='Brown Eyed Woman', duration=datetime.timedelta(seconds=287), artist=a, record=r)
		response = self.client.post('/api/v1/songs/1/update/', {'name':'Terrapin'})
		song = Song.objects.get(id=1)
		self.assertNotContains(response, 'Brown')
		self.assertEquals(song.name, 'Terrapin')

	def test_update_listing(self):
		self.assertEquals(Listing.objects.all().exists(), False) # DB currently empty
		seller = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='pass2')
		buyer = User.objects.create(first_name='Kate', last_name='Shea', email='kateshea@test.com', passwordHash='pass3')
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Listing.objects.create(price=55, seller=seller, buyer=buyer, record=r, date_posted=datetime.date.today())
		response = self.client.post('/api/v1/listings/1/update/', {'price':150})
		listing = Listing.objects.get(id=1)
		self.assertNotContains(response, 55)
		self.assertEquals(listing.price, 150)


class DeleteTestCases(TransactionTestCase):
	def test_delete_user(self):
		self.assertEquals(User.objects.all().exists(), False) # DB currently empty
		User.objects.create(first_name='James', last_name='Robins', email='jamesrobins@test.com', passwordHash='pass4')
		self.assertEquals(User.objects.all().exists(), True)
		response = self.client.post('/api/v1/users/1/delete/')
		self.assertContains(response, 'Robins')
		self.assertEquals(User.objects.all().exists(), False)

	def test_delete_artist(self):
		self.assertEquals(Artist.objects.all().exists(), False) # DB currently empty
		Artist.objects.create(name='The Grateful Dead')
		self.assertEquals(Artist.objects.all().exists(), True)
		response = self.client.post('/api/v1/artists/1/delete/')
		self.assertContains(response, 'The Grateful Dead')
		self.assertEquals(Artist.objects.all().exists(), False)

	def test_delete_record(self):
		self.assertEquals(User.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		self.assertEquals(Record.objects.all().exists(), True)
		response = self.client.post('/api/v1/records/1/delete/')
		self.assertContains(response, 'Terrapin')
		self.assertEquals(Record.objects.all().exists(), False)

	def test_delete_song(self):
		self.assertEquals(Song.objects.all().exists(), False) # DB currently empty
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Song.objects.create(name='Brown Eyed Woman', duration=datetime.timedelta(seconds=287), artist=a, record=r)
		self.assertEquals(Song.objects.all().exists(), True)
		response = self.client.post('/api/v1/songs/1/delete/')
		self.assertContains(response, 'Brown Eyed')
		self.assertEquals(Song.objects.all().exists(), False)

	def test_delete_listing(self):
		self.assertEquals(Listing.objects.all().exists(), False) # DB currently empty
		seller = User.objects.create(first_name='Jane', last_name='Doe', email='janedoe@test.com', passwordHash='pass2')
		buyer = User.objects.create(first_name='Kate', last_name='Shea', email='kateshea@test.com', passwordHash='pass3')
		a = Artist.objects.create(name='The Grateful Dead')
		r = Record.objects.create(name='Terrapin Station', artist=a, release_date=datetime.date.today(), pressing='test')
		Listing.objects.create(price=55, seller=seller, buyer=buyer, record=r, date_posted=datetime.date.today())
		self.assertEquals(Listing.objects.all().exists(), True)
		response = self.client.post('/api/v1/listings/1/delete/')
		self.assertContains(response, 55)
		self.assertEquals(Listing.objects.all().exists(), False)
