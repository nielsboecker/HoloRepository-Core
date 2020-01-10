import tarfile
import unittest

import requests

from server import app


class FlaskTestCase(unittest.TestCase):
    def test_the_post_request_without_file_is_not_allowed(self):
        tester = app.test_client(self)
        response = tester.post("/model")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
