import unittest
from aws_allowlister.shared.utils import clean_service_name


class UtilsTestCase(unittest.TestCase):
    def test_utils(self):
        result = clean_service_name('\n\n\t\tAmazon API Gateway\t\n')
        self.assertEqual(result, "Amazon API Gateway")
        result = clean_service_name('Amazon API Gateway\n')
        self.assertTrue(result == "Amazon API Gateway")
