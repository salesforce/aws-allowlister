import unittest
from aws_allowlister.scrapers.overrides import Overrides


class OverridesTestCase(unittest.TestCase):
    def test_overrides(self):
        overrides = Overrides()
        result = overrides.get_iam_names_matching_sdk_name("ec2")
        expected_result = [
            "ec2",
            "ebs"
        ]
        self.assertEqual(result, expected_result)

        result = overrides.get_iam_names_matching_service_name("AWS Web Application Firewall")
        expected_result = [
            "waf",
            "wafv2",
            "waf-regional"
        ]
        self.assertEqual(result, expected_result)
