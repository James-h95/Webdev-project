"""
Selenium Tests
"""
localhost = "http://localhost:5000/"

import unittest
from unittest import TestCase
from application import create_app, db
from application.models import User, Game, UserGames
from application.config import Config
from application.test.test_utlis import add_test_data_to_db

from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import multiprocessing
import time

localhost = 'http://localhost:5000/'

class SeleniumTests(TestCase):
  @classmethod
  def setUp(self):
    self.testApp = create_app(config=TestConfig) #create app instance with TestConfig
    self.app_context = self.testApp.app_context()
    self.app_context.push()
    db.create_all()
    add_test_data_to_db()

    self.server_thread = multiprocessing.Process(target = self.testApp.run)
    self.server_thread.start()

    self.driver = webdriver.Chrome()
    self.driver.get(localhost)

  @classmethod
  def tearDown(self):
    self.server_thread.terminate()
    self.driver.close()
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test_login_page(self):
        #  Checking the login functionality
        self.driver.get("http://localhost:5000/login")  # Update URL based on your route configuration
        username_input = self.driver.find_element_by_name("username")
        password_input = self.driver.find_element_by_name("password")
        submit_button = self.driver.find_element_by_xpath("//input[@type='submit']")
        
        username_input.send_keys("testuser")
        password_input.send_keys("password")
        submit_button.click()
        
        # Assert to check if login was successful
        success_message = self.driver.find_element_by_class_name("success").text
        self.assertIn("Welcome, testuser", success_message)


if __name__ == '__main__':
    unittest.main()



# to run the test: python -m unittest discover -s test -p "test_web.py"
