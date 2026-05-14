import unittest
from app import create_app, db
from app.config import TestConfig
from app.models import User, CoffeeLog, Message
import json


def add_test_data_to_db():
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)

    user2 = User(username='testuser2', email='test2@test.com')
    user2.set_password('password123')
    db.session.add(user2)

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

    # Test 1: checks coffee log is saved correctly to the db
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

    # Test 2: Checks that user is logged in before they can access the log coffee page
    def test_log_coffee_requires_login(self):
        response = self.client.get('/log-coffee', follow_redirects=False)
        self.assertEqual(response.status_code, 302, 'Unauthenticated user should be redirected')
        self.assertIn('/', response.location, 'Should redirect to login page')


class MessagingTests(unittest.TestCase):

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

    def login(self, email='test@test.com', password='password123'):
        return self.client.post('/', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    # Test 3: Messages page requires login
    def test_messages_requires_login(self):
        response = self.client.get('/messages', follow_redirects=False)
        self.assertEqual(response.status_code, 302,
                         'Unauthenticated user should be redirected from messages')

    # Test 4: Messages page loads for logged-in user
    def test_messages_page_loads(self):
        self.login()
        response = self.client.get('/messages')
        self.assertEqual(response.status_code, 200,
                         'Messages page should load for authenticated user')

    # Test 5: Message is saved to database
    def test_message_saved_to_db(self):
        user1 = User.query.filter_by(username='testuser').first()
        user2 = User.query.filter_by(username='testuser2').first()

        msg = Message(
            sender_id=user1.id,
            receiver_id=user2.id,
            body='Hello from test!'
        )
        db.session.add(msg)
        db.session.commit()

        saved = Message.query.filter_by(body='Hello from test!').first()
        self.assertIsNotNone(saved, 'Message should be saved to the database')
        self.assertEqual(saved.sender_id, user1.id, 'Sender should be user1')
        self.assertEqual(saved.receiver_id, user2.id, 'Receiver should be user2')
        self.assertFalse(saved.read, 'New message should be unread by default')

    # Test 6: Send message via API
    def test_api_send_message(self):
        self.login()
        user2 = User.query.filter_by(username='testuser2').first()

        response = self.client.post(
            f'/api/messages/{user2.id}/send',
            data=json.dumps({'body': 'Test API message'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Send message API should return 200')
        self.assertTrue(data['success'], 'Send message should return success=True')
        self.assertEqual(data['message']['body'], 'Test API message',
                         'Returned message body should match sent body')

    # Test 7: Fetch messages via API
    def test_api_get_messages(self):
        self.login()
        user2 = User.query.filter_by(username='testuser2').first()

        self.client.post(
            f'/api/messages/{user2.id}/send',
            data=json.dumps({'body': 'Hello!'}),
            content_type='application/json'
        )

        response = self.client.get(f'/api/messages/{user2.id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Get messages API should return 200')
        self.assertIn('messages', data, 'Response should contain messages key')
        self.assertEqual(len(data['messages']), 1, 'Should have 1 message')
        self.assertEqual(data['messages'][0]['body'], 'Hello!', 'Message body should match')

    # Test 8: Empty message body is rejected
    def test_api_send_empty_message_rejected(self):
        self.login()
        user2 = User.query.filter_by(username='testuser2').first()

        response = self.client.post(
            f'/api/messages/{user2.id}/send',
            data=json.dumps({'body': '   '}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400, 'Empty message should return 400')
        self.assertFalse(data['success'], 'Empty message should return success=False')

    # Test 9: Unread count API returns correct value
    def test_api_unread_count(self):
        self.login()
        response = self.client.get('/api/messages/unread')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Unread count API should return 200')
        self.assertIn('unread', data, 'Response should contain unread key')
        self.assertEqual(data['unread'], 0, 'New user should have 0 unread messages')

    # Test 10: Messages are marked as read when fetched
    def test_messages_marked_as_read(self):
        user1 = User.query.filter_by(username='testuser').first()
        user2 = User.query.filter_by(username='testuser2').first()

        msg = Message(sender_id=user2.id, receiver_id=user1.id, body='Hey!', read=False)
        db.session.add(msg)
        db.session.commit()

        self.login(email='test@test.com')
        self.client.get(f'/api/messages/{user2.id}')

        updated = Message.query.get(msg.id)
        self.assertTrue(updated.read, 'Message should be marked as read after being fetched')


class ExploreTests(unittest.TestCase):

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

    def login(self):
        return self.client.post('/', data={
            'email': 'test@test.com',
            'password': 'password123'
        }, follow_redirects=True)

    # Test 11: Explore page requires login
    def test_explore_requires_login(self):
        response = self.client.get('/explore', follow_redirects=False)
        self.assertEqual(response.status_code, 302,
                         'Unauthenticated user should be redirected from explore')

    # Test 12: Explore page loads for logged-in user
    def test_explore_page_loads(self):
        self.login()
        response = self.client.get('/explore')
        self.assertEqual(response.status_code, 200,
                         'Explore page should load for authenticated user')

    # Test 13: Match API returns failure when user has no logs
    def test_match_api_no_logs(self):
        self.login()
        response = self.client.get('/api/match')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 'Match API should return 200')
        self.assertFalse(data['success'],
                         'Match should fail when user has no coffee logs')

    # Test 14: Match API finds users with same coffee type
    def test_match_api_finds_shared_coffee(self):
        user1 = User.query.filter_by(username='testuser').first()
        user2 = User.query.filter_by(username='testuser2').first()

        db.session.add(CoffeeLog(cafe_name='Cafe A', coffee_type='Latte',
                                  rating=4, user_id=user1.id))
        db.session.add(CoffeeLog(cafe_name='Cafe B', coffee_type='Latte',
                                  rating=5, user_id=user2.id))
        db.session.commit()

        self.login()
        response = self.client.get('/api/match?coffee_type=Latte')
        data = json.loads(response.data)
        self.assertTrue(data['success'], 'Match should succeed when users share a coffee type')
        self.assertEqual(len(data['matches']), 1, 'Should find exactly 1 match')
        self.assertEqual(data['matches'][0]['username'], 'testuser2',
                         'Matched user should be testuser2')

    # Test 15: Match API finds users at same cafe (partial match)
    def test_match_api_finds_shared_cafe(self):
        user1 = User.query.filter_by(username='testuser').first()
        user2 = User.query.filter_by(username='testuser2').first()

        db.session.add(CoffeeLog(cafe_name='Telegram Coffee', coffee_type='Latte',
                                  rating=4, user_id=user1.id))
        db.session.add(CoffeeLog(cafe_name='Telegram Coffee', coffee_type='Espresso',
                                  rating=5, user_id=user2.id))
        db.session.commit()

        self.login()
        response = self.client.get('/api/match?cafe_name=Telegram')
        data = json.loads(response.data)
        self.assertTrue(data['success'], 'Match should succeed when users share a cafe')
        self.assertEqual(data['matches'][0]['username'], 'testuser2',
                         'Matched user should be testuser2')


if __name__ == '__main__':
    unittest.main()