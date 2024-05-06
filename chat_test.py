import unittest
from chat import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_document_upload(self):
        response = self.app.post('/upload', data={'file': (BytesIO(b'my file contents'), 'test.txt')})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Document uploaded successfully', response.data)

    def test_session_start(self):
        response = self.app.post('/start_session')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Session started successfully', response.data)

    def test_chat_message(self):
        response = self.app.post('/chat', data={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Response received successfully', response.data)

if __name__ == '__main__':
    unittest.main()
