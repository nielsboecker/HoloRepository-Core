from app import app

import unittest

class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester=app.test_client(self)
        response = tester.post('/seg')
        self.assertEqual(response.status_code, 400)

    def test_file(self):
        tester=app.test_client(self)
        f= open('c_CT.nii', 'rb') 
        response = tester.post('/seg',data={'file': f})
        f.close()
        self.assertEqual(response.status_code, 200)

if __name__=='__main__':
    unittest.main()

