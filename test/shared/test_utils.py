import json
import unittest
from aws_allowlister.shared.utils import clean_service_name, get_service_name_matching_iam_service_prefix


class UtilsTestCase(unittest.TestCase):
    def test_get_service_name_matching_iam_service_prefix(self):
        iam_service_prefix = "s3"
        result = get_service_name_matching_iam_service_prefix(iam_service_prefix)
        print(json.dumps(result, indent=4))
        self.assertEqual(result, "Amazon S3")

        service_name_pairs = {
            "a4b": "Alexa for Business",
            "access-analyzer": "IAM Access Analyzer",
            "account": "AWS Accounts",
            "acm": "AWS Certificate Manager"
            # .. etc.
            #   Try opening the SQLite database in DB Browser for SQLite to examine it more.
            #   And view the table called compliancetable
        }
        for iam_service_prefix in list(service_name_pairs.keys()):
            # service prefix is like a4b, access-analzer, etc.
            result = get_service_name_matching_iam_service_prefix(iam_service_prefix)
            self.assertEqual(result, service_name_pairs.get(iam_service_prefix))
            print(f"{iam_service_prefix}: {result}")

    # def test_chomp(self):
    #     print()
    #
    # def test_normalize_tags_or_strings(self):
    #     print()

    def test_clean_service_name_non_breaking_spaces(self):
        result = clean_service_name('AWS Amplify\u00a0')
        self.assertEqual(result, "AWS Amplify")

    def test_clean_service_name_remove_text_after_bracket(self):
        # Example: Amazon Aurora on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
        result = clean_service_name('Amazon Aurora [MySQL, PostgreSQL]')
        self.assertEqual(result, "Amazon Aurora")

    def test_clean_service_name_remove_text_after_parentheses(self):
        # Example: Alexa for Business on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
        result = clean_service_name('Alexa for Business (for healthcare skills only – requires Alexa Skills BAA. See '
                                    'HIPAA whitepaper for details)')
        self.assertEqual(result, "Alexa for Business")

    def test_clean_service_name_tabs_and_newlines(self):
        # Make sure tabs and newlines are removed properly
        result = clean_service_name('\n\n\t\tAmazon API Gateway\t\n')
        self.assertEqual(result, "Amazon API Gateway")
        result = clean_service_name('Amazon API Gateway\n')
        self.assertTrue(result == "Amazon API Gateway")


