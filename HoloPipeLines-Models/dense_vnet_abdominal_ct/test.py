from server import app

import unittest

class FlaskTestCase(unittest.TestCase):
    def test_the_post_request_without_file_is_not_allowed(self):
        tester=app.test_client(self)
        response = tester.post('/model')
        self.assertEqual(response.status_code, 400)

    def test_the_post_request_with_file_can_be_successed(self):
        tester=app.test_client(self)
        f= open('c_CT.nii', 'rb') 
        response = tester.post('/model',data={'file': f})
        f.close()
        self.assertEqual(response.status_code, 200)

if __name__=='__main__':
    unittest.main()