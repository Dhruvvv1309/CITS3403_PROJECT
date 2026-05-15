import unittest
import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import create_app, db
from app.config import TestConfig

localHost = "http://127.0.0.1:5000/"

class CoffeeLogSeleniumTests(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()
        time.sleep(2)

        self.driver = webdriver.Chrome()
        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()