from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase
import unittest

class MyTests(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Remote(
			command_executor='http://selenium-chrome:4444/wd/hub',
			desired_capabilities=DesiredCapabilities.CHROME)

	def test_recent_listings(self):
		driver = self.driver

		# go to home page
		driver.get("http://web:8000/home/")

		# find elements containing two listings
		listing0 = driver.find_element_by_id('listing0')
		listing1 = driver.find_element_by_id('listing1')

		# get listing0 info
		record0 = listing0.find_element_by_id('record').text
		date0 = listing0.find_element_by_id('date').text
		buyer0 = listing0.find_element_by_id('buyer').text
		seller0 = listing0.find_element_by_id('seller').text
		price0 = listing0.find_element_by_id('price').text

		# get listing1 info
		record1 = listing1.find_element_by_id('record').text
		date1 = listing1.find_element_by_id('date').text
		buyer1 = listing1.find_element_by_id('buyer').text
		seller1 = listing1.find_element_by_id('seller').text
		price1 = listing1.find_element_by_id('price').text

		self.assertEqual(record0, 'Amen')
		self.assertEqual(date0, '2018-01-15')
		self.assertEqual(buyer0, 'Buyer: Josh Gross')
		self.assertEqual(seller0, 'Seller: Julia Suozzi')
		self.assertEqual(price0, 'Price: $1000.32')

		self.assertEqual(record1, 'To Pimp A Butterfly')
		self.assertEqual(date1, '2015-12-10')
		self.assertEqual(buyer1, 'Buyer: James Johnston')
		self.assertEqual(seller1, 'Seller: Josh Gross')
		self.assertEqual(price1, 'Price: $19.99')

	def test_create_account(self):
		driver = self.driver
		driver.get("http://web:8000/createAccount/")
		form = driver.find_element_by_id('createAccountForm')
		first_name = form.find_element_by_id('id_first_name')
		last_name = form.find_element_by_id('id_last_name')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_passwordHash')

		first_name.send_keys("New")
		last_name.send_keys("User")
		email.send_keys("testemail@test.com")
		password.send_keys("testpassword")
		email.submit()
		assert("login" in driver.page_source)

	def test_create_account_with_unavailable_email(self):
		driver = self.driver
		driver.get("http://web:8000/createAccount/")
		form = driver.find_element_by_id('createAccountForm')
		first_name = form.find_element_by_id('id_first_name')
		last_name = form.find_element_by_id('id_last_name')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_passwordHash')

		first_name.send_keys("New")
		last_name.send_keys("User")
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()
		assert("This email is already in use. Please try again." in driver.page_source)

	def test_succesful_login(self):
		driver = self.driver
		driver.get("http://web:8000/login/")
		form = driver.find_element_by_id('loginForm')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_password')
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()
		assert("Home Page" in driver.page_source)
	
	def test_unsuccessful_login(self):
		driver = self.driver
		driver.get("http://web:8000/login/")
		form = driver.find_element_by_id('loginForm')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_password')
		email.send_keys("fake@email.com")
		password.send_keys("test")
		email.submit()
		assert("Incorrect email or password. Please try again." in driver.page_source)

	def test_create_listing_not_logged_in(self):
		driver = self.driver
		driver.get("http://web:8000/createListing/")
		assert("You must be logged in to create a listing" in driver.page_source)

	def test_already_logged_in(self):
		driver = self.driver
		driver.get("http://web:8000/login/")
		form = driver.find_element_by_id('loginForm')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_password')
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()
		assert("Home Page" in driver.page_source)
		driver.get("http://web:8000/login/")
		assert("You are already logged in." in driver.page_source)

	def test_log_out(self):
		driver = self.driver
		driver.get("http://web:8000/login/")
		form = driver.find_element_by_id('loginForm')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_password')
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()
		driver.get("http://web:8000/logout/")
		assert("Successfully logged out!" in driver.page_source)

	def test_already_logged_out(self):
		driver = self.driver
		driver.get("http://web:8000/login/")
		form = driver.find_element_by_id('loginForm')
		email = form.find_element_by_id('id_email')
		password = form.find_element_by_id('id_password')
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()
		driver.get("http://web:8000/logout/")
		driver.get("http://web:8000/logout/")
		assert("You are not logged in." in driver.page_source)

	def test_create_listing_succesful(self):
		driver = self.driver
		driver.get("http://web:8000/createListing/")
		loginForm = driver.find_element_by_id('loginForm')
		email = loginForm.find_element_by_id('id_email')
		password = loginForm.find_element_by_id('id_password')
		email.send_keys("jps4nf@virginia.edu")
		password.send_keys("password")
		email.submit()

		driver.get("http://web:8000/createListing/")
		listingForm = driver.find_element_by_id('createListingForm')
		price = listingForm.find_element_by_id('id_price')
		record = listingForm.find_element_by_id('id_record')
		darkSideOfMoon = record.find_elements_by_tag_name("option")[2]
		darkSideOfMoon.click()
		condition = listingForm.find_element_by_id('id_condition')
		fair = condition.find_elements_by_tag_name("option")[5]
		fair.click()
		fair.submit()
		assert("You must be logged in to create a listing" not in driver.page_source)

	def tearDown(self):
		self.driver.close()
		

if __name__ == "__main__":
	unittest.main()
