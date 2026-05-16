import unittest
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from app import create_app, db
from app.config import TestConfig
from app.models import User, CoffeeLog

localHost = "http://127.0.0.1:5000/"

def add_test_data_to_db():
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

class SeleniumBaseTest(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.user = add_test_data_to_db()

        # Use threading on Mac, multiprocessing on Windows/Linux
        if sys.platform == 'darwin':
            import threading
            def run_app():
                with self.testApp.app_context():
                    self.testApp.run()
            self.server_thread = threading.Thread(target=run_app)
            self.server_thread.daemon = True
            self.server_thread.start()
        else:
            import multiprocessing
            self.server_thread = multiprocessing.Process(target=self.testApp.run)
            self.server_thread.start()

        time.sleep(2)

        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        if sys.platform != 'darwin':
            self.server_thread.terminate()
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        # Delete the test database file
        import os
        if os.path.exists('test.db'):
            os.remove('test.db')

    def login(self):
        self.driver.get(localHost)
        self.wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("test@test.com")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "submit").click()
        self.wait.until(lambda driver: "my_journal" in driver.current_url or "My Journal" in driver.page_source)


class CoffeeLogSeleniumTests(SeleniumBaseTest):

    # Test: Log coffee page loads after login
    def test_log_coffee_page_loads(self):
        self.login()

        # Navigate to log coffee page
        self.driver.get(localHost + "log-coffee")
        time.sleep(1)

        # Check we are on the right page
        self.assertIn("log-coffee", self.driver.current_url)
        self.assertIn("drinking", self.driver.page_source.lower())

    # Test: User can submit the log coffee form
    def test_log_coffee_form_submit(self):
        self.login()

        # Navigate to log coffee page
        self.driver.get(localHost + "log-coffee")
        time.sleep(1)

        # Fill in the form using JavaScript clicks to avoid sticky header interception
        cafe_name = self.driver.find_element(By.ID, "cafeName")
        self.driver.execute_script("arguments[0].value = 'Test Cafe';", cafe_name)

        # Select coffee type from dropdown
        Select(self.driver.find_element(By.ID, "coffeeType")).select_by_value("latte")

        # Click the 3rd star for rating
        stars = self.driver.find_elements(By.CLASS_NAME, "star")
        self.driver.execute_script("arguments[0].click();", stars[2])

        # Fill in notes
        notes = self.driver.find_element(By.ID, "notes")
        self.driver.execute_script("arguments[0].value = 'Great coffee!';", notes)

        # Submit the form
        submit = self.driver.find_element(By.NAME, "submit")
        self.driver.execute_script("arguments[0].click();", submit)
        time.sleep(1)

        # Check the coffee log was saved to the database
        with self.testApp.app_context():
            log = CoffeeLog.query.filter_by(cafe_name="Test Cafe").first()
            self.assertIsNotNone(log, "Coffee log should be saved to the database")
            self.assertEqual(log.coffee_type, "latte")
            self.assertEqual(log.rating, 3)


if __name__ == '__main__':
    unittest.main()
