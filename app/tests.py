import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import User, CoffeeLog

def add_test_data_to_db():
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

class CoffeeLogTests(unittest.TestCase):

    def setUp(self):
        test_app = create_app(TestConfig)
        self.app_context = test_app.app_context()
        self.app_context.push()
        self.client = test_app.test_client()
        db.create_all()
        add_test_data_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
#Test 1: checks coffee log is saved correctly to the db
    def test_coffee_log_saved_to_db(self):
        user = User.query.filter_by(username='testuser').first()
        entry = CoffeeLog(
            cafe_name='Test Cafe',
            coffee_type='latte',
            rating=4,
            notes='Test notes',
            user_id=user.id
        )
        db.session.add(entry)
        db.session.commit()

        saved = CoffeeLog.query.filter_by(cafe_name='Test Cafe').first()
        self.assertIsNotNone(saved, 'Coffee log entry should be saved to the database')
        self.assertEqual(saved.rating, 4, 'Rating should equal 4')
        self.assertEqual(saved.user_id, user.id, 'Coffee log should be linked to the correct user')
#Test 2: Checks that user is logged in before they can access the log coffee page
    def test_log_coffee_requires_login(self):
        response = self.client.get('/log-coffee', follow_redirects=False)
        self.assertEqual(response.status_code, 302, 'Unauthenticated user should be redirected')
        self.assertIn('/', response.location, 'Should redirect to login page')

if __name__ == '__main__':
    unittest.main()