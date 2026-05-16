import unittest
import threading
import time
import os
import tempfile
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from app import create_app, db
from app.config import TestConfig
from app.models import User, CoffeeLog, Message

# ── Shared server for Messages/Explore tests (port 5001, headless) ──
BASE_URL = 'http://127.0.0.1:5001'

_driver     = None
_app        = None
_ctx        = None
_db_path    = None


def setUpModule():
    """Runs once before ALL tests in this file."""
    global _driver, _app, _ctx, _db_path

    _db_fd, _db_path = tempfile.mkstemp(suffix='.db')
    os.close(_db_fd)

    class SeleniumConfig:
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{_db_path}'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TESTING = True
        WTF_CSRF_ENABLED = False
        SECRET_KEY = 'selenium-test-secret'
        UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')

    _app = create_app(SeleniumConfig)
    _ctx = _app.app_context()
    _ctx.push()

    db.create_all()

    u1 = User(username='selenium_user1', email='sel1@test.com')
    u1.set_password('password123')
    u2 = User(username='selenium_user2', email='sel2@test.com')
    u2.set_password('password123')
    db.session.add_all([u1, u2])
    db.session.commit()

    t = threading.Thread(
        target=_app.run,
        kwargs={'port': 5001, 'use_reloader': False, 'debug': False, 'threaded': True}
    )
    t.daemon = True
    t.start()
    time.sleep(2)

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1280,900')

    _driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    _driver.implicitly_wait(5)


def tearDownModule():
    global _driver, _ctx, _db_path

    if _driver:
        _driver.quit()
    if _ctx:
        db.session.remove()
        db.drop_all()
        _ctx.pop()
    if _db_path and os.path.exists(_db_path):
        try:
            os.unlink(_db_path)
        except Exception:
            pass


class SeleniumBase(unittest.TestCase):
    """Base class for Messages/Explore UI tests — uses shared headless driver."""

    def setUp(self):
        self.driver = _driver
        self.wait   = WebDriverWait(_driver, 10)

    def login(self, email='sel1@test.com', password='password123'):
        self.driver.get(f'{BASE_URL}/')
        self.wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'password').clear()
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
        self.wait.until(EC.url_contains('/my_journal'))

    def logout(self):
        self.driver.get(f'{BASE_URL}/logout')
        self.wait.until(EC.url_contains('/'))


# ════════════════════════════════════════════
#  MESSAGES UI TESTS
# ════════════════════════════════════════════

class TestMessagesUI(SeleniumBase):

    # Selenium Test 1: Nav has Messages link
    def test_messages_link_in_nav(self):
        self.login()
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, '.nav-links a')
        nav_texts = [link.text for link in nav_links]
        self.assertIn('Messages', nav_texts,
                      'Messages link should appear in the nav bar')

    # Selenium Test 2: Messages page loads with correct heading
    def test_messages_page_heading(self):
        self.login()
        self.driver.get(f'{BASE_URL}/messages')
        heading = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.panel-heading'))
        )
        self.assertEqual(heading.text, 'Messages',
                         'Messages page should show "Messages" heading')

    # Selenium Test 3: Unauthenticated user redirected from messages
    def test_messages_redirects_when_logged_out(self):
        self.logout()
        self.driver.get(f'{BASE_URL}/messages')
        self.wait.until(EC.url_contains('/'))
        self.assertNotIn('/messages', self.driver.current_url,
                         'Logged out user should be redirected away from messages')

    # Selenium Test 4: Conversation sidebar shows other users
    def test_messages_sidebar_shows_users(self):
        self.login()
        self.driver.get(f'{BASE_URL}/messages')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.conv-list')))
        conv_items = self.driver.find_elements(By.CSS_SELECTOR, '.conv-item')
        self.assertGreater(len(conv_items), 0,
                           'Sidebar should show at least one user to message')

    # Selenium Test 5: Clicking a user opens the chat panel
    def test_clicking_user_opens_chat(self):
        self.login()
        self.driver.get(f'{BASE_URL}/messages')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.conv-item')))
        self.driver.find_element(By.CSS_SELECTOR, '.conv-item').click()
        chat_active = self.wait.until(EC.visibility_of_element_located((By.ID, 'chatActive')))
        self.assertTrue(chat_active.is_displayed(),
                        'Chat panel should be visible after clicking a user')

    # Selenium Test 6: Message input and send button are present
    def test_message_composer_present(self):
        self.login()
        self.driver.get(f'{BASE_URL}/messages')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.conv-item')))
        self.driver.find_element(By.CSS_SELECTOR, '.conv-item').click()
        self.wait.until(EC.visibility_of_element_located((By.ID, 'msgInput')))
        msg_input = self.driver.find_element(By.ID, 'msgInput')
        send_btn  = self.driver.find_element(By.CSS_SELECTOR, '.send-btn')
        self.assertTrue(msg_input.is_displayed(), 'Message input should be visible')
        self.assertTrue(send_btn.is_displayed(),  'Send button should be visible')

    # Selenium Test 7: Sending a message shows it in the chat
    def test_send_message_appears_in_chat(self):
        self.login()
        self.driver.get(f'{BASE_URL}/messages')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.conv-item')))
        self.driver.find_element(By.CSS_SELECTOR, '.conv-item').click()
        self.wait.until(EC.visibility_of_element_located((By.ID, 'msgInput')))
        msg_input = self.driver.find_element(By.ID, 'msgInput')
        msg_input.send_keys('Hello from Selenium!')
        msg_input.send_keys(Keys.RETURN)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-row.sent')))
        sent_bubbles = self.driver.find_elements(By.CSS_SELECTOR, '.msg-row.sent .bubble')
        texts = [b.text for b in sent_bubbles]
        self.assertTrue(any('Hello from Selenium!' in t for t in texts),
                        'Sent message should appear in the chat')


# ════════════════════════════════════════════
#  EXPLORE UI TESTS
# ════════════════════════════════════════════

class TestExploreUI(SeleniumBase):

    # Selenium Test 8: Explore page loads with hero heading
    def test_explore_page_hero(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        hero = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.explore-hero h1'))
        )
        self.assertIn('brewing', hero.text.lower(),
                      'Explore hero heading should contain "brewing"')

    # Selenium Test 9: Unauthenticated user redirected from explore
    def test_explore_redirects_when_logged_out(self):
        self.logout()
        self.driver.get(f'{BASE_URL}/explore')
        self.wait.until(EC.url_contains('/'))
        self.assertNotIn('/explore', self.driver.current_url,
                         'Logged out user should be redirected away from explore')

    # Selenium Test 10: Find My Match button is present
    def test_find_match_button_present(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        btn = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Find My Match')]")
            )
        )
        self.assertTrue(btn.is_displayed(), 'Find My Match button should be visible')

    # Selenium Test 11: Coffee type dropdown has correct options
    def test_coffee_dropdown_options(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        self.wait.until(EC.presence_of_element_located((By.ID, 'matchCoffee')))
        options = self.driver.find_elements(By.CSS_SELECTOR, '#matchCoffee option')
        option_texts = [o.text for o in options]
        self.assertIn('Latte',      option_texts, 'Latte should be an option')
        self.assertIn('Espresso',   option_texts, 'Espresso should be an option')
        self.assertIn('Cold Brew',  option_texts, 'Cold Brew should be an option')
        self.assertIn('Cappuccino', option_texts, 'Cappuccino should be an option')

    # Selenium Test 12: Clicking Find My Match shows a result or no-match message
    def test_find_match_shows_response(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Find My Match')]")
            )
        )
        btn.click()
        self.wait.until(
            lambda d: (
                d.find_element(By.ID, 'matchResults').is_displayed() or
                d.find_element(By.ID, 'matchNone').is_displayed()
            )
        )
        results_visible = self.driver.find_element(By.ID, 'matchResults').is_displayed()
        none_visible    = self.driver.find_element(By.ID, 'matchNone').is_displayed()
        self.assertTrue(results_visible or none_visible,
                        'Either match results or no-match message should appear')

    # Selenium Test 13: Community section shows other users
    def test_community_section_shows_users(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.user-grid')))
        user_cards = self.driver.find_elements(By.CSS_SELECTOR, '.user-card')
        self.assertGreater(len(user_cards), 0,
                           'Community section should show at least one user card')

    # Selenium Test 14: Message button on user card links to messages page
    def test_message_button_links_to_messages(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.view-btn')))
        self.driver.find_element(By.CSS_SELECTOR, '.view-btn').click()
        self.wait.until(EC.url_contains('/messages'))
        self.assertIn('/messages', self.driver.current_url,
                      'Message button should navigate to the messages page')

    # Selenium Test 15: Map section exists in the DOM
    def test_map_section_present(self):
        self.login()
        self.driver.get(f'{BASE_URL}/explore')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.map-section')))
        self.driver.execute_script(
            'document.querySelector(".map-section").scrollIntoView(true);'
        )
        time.sleep(0.5)
        exists = self.driver.execute_script(
            'return document.querySelector(".map-section") !== null'
        )
        self.assertTrue(exists, 'Perth CBD map section should exist on the explore page')


# ════════════════════════════════════════════
#  COFFEE LOG SELENIUM TESTS (teammates)
# ════════════════════════════════════════════

LOCAL_HOST = 'http://127.0.0.1:5000/'


def add_test_data_to_db():
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


class SeleniumBaseTest(unittest.TestCase):
    """Base class for CoffeeLog Selenium tests — uses visible Chrome on port 5000."""

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.user = add_test_data_to_db()

        if sys.platform == 'darwin':
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
        if os.path.exists('test.db'):
            os.remove('test.db')

    def login(self):
        self.driver.get(LOCAL_HOST)
        self.wait.until(
            EC.presence_of_element_located((By.NAME, 'email'))
        ).send_keys('test@test.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password123')
        self.driver.find_element(By.NAME, 'submit').click()
        self.wait.until(
            lambda d: 'my_journal' in d.current_url or 'My Journal' in d.page_source
        )


class CoffeeLogSeleniumTests(SeleniumBaseTest):

    # Selenium Test: Log coffee page loads after login
    def test_log_coffee_page_loads(self):
        self.login()
        self.driver.get(LOCAL_HOST + 'log-coffee')
        time.sleep(1)
        self.assertIn('log-coffee', self.driver.current_url)
        self.assertIn('drinking', self.driver.page_source.lower())

    # Selenium Test: User can submit the log coffee form
    def test_log_coffee_form_submit(self):
        self.login()
        self.driver.get(LOCAL_HOST + 'log-coffee')
        time.sleep(1)

        cafe_name = self.driver.find_element(By.ID, 'cafeName')
        self.driver.execute_script("arguments[0].value = 'Test Cafe';", cafe_name)

        Select(self.driver.find_element(By.ID, 'coffeeType')).select_by_value('latte')

        stars = self.driver.find_elements(By.CLASS_NAME, 'star')
        self.driver.execute_script('arguments[0].click();', stars[2])

        notes = self.driver.find_element(By.ID, 'notes')
        self.driver.execute_script("arguments[0].value = 'Great coffee!';", notes)

        submit = self.driver.find_element(By.NAME, 'submit')
        self.driver.execute_script('arguments[0].click();', submit)
        time.sleep(1)

        with self.testApp.app_context():
            log = CoffeeLog.query.filter_by(cafe_name='Test Cafe').first()
            self.assertIsNotNone(log, 'Coffee log should be saved to the database')
            self.assertEqual(log.coffee_type, 'latte')
            self.assertEqual(log.rating, 3)


if __name__ == '__main__':
    unittest.main()