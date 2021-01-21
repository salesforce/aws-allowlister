import unittest
from aws_allowlister.shared.utils import clean_service_name


class UtilsTestCase(unittest.TestCase):
    def test_get_service_name_matching_iam_service_prefix(self):
        print()

    def test_chomp(self):
        print()

    def test_normalize_tags_or_strings(self):
        print()

    def test_clean_service_name(self):
        result = clean_service_name('\n\n\t\tAmazon API Gateway\t\n')
        self.assertEqual(result, "Amazon API Gateway")
        result = clean_service_name('Amazon API Gateway\n')
        self.assertTrue(result == "Amazon API Gateway")


