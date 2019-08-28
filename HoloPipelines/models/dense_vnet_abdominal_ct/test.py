import tarfile
import unittest

import requests

from server import app


class FlaskTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = "https://www.dropbox.com/s/5fk0m9v12if5da9/dense_vnet_abdominal_ct_model_zoo_data.tar.gz?dl=1"
        r = requests.get(url, allow_redirects=True)
        open("dense_vnet_abdominal_ct_model_zoo_data.tar.gz", "wb").write(r.content)
        fname = "dense_vnet_abdominal_ct_model_zoo_data.tar.gz"
        if fname.endswith("tar.gz"):
            tar = tarfile.open(fname, "r:gz")
            tar.extractall()
            tar.close()
        elif fname.endswith("tar"):
            tar = tarfile.open(fname, "r:")
            tar.extractall()
            tar.close()

    def test_the_post_request_without_file_is_not_allowed(self):
        tester = app.test_client(self)
        response = tester.post("/model")
        self.assertEqual(response.status_code, 400)

    def test_the_post_request_with_file_can_be_succeed(self):
        tester = app.test_client(self)
        f = open("100_CT.nii", "rb")
        response = tester.post("/model", data={"file": f})
        f.close()
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
