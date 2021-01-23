import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class HipaaQATestCase(unittest.TestCase):
    def test_gh_07_HIPAA_compliant_services(self):
        results = compliance_data.get_compliant_services(
            db_session=db_session, compliance_standard="HIPAA"
        )
        expected_results = [
            "a4b",
            "elasticloadbalancing",
            "healthlake",
            "macie",
            "mobiletargeting"
        ]
        print(len(results))
        for expected_result in expected_results:
            print(f"{expected_result}: in {expected_result in results}")
            self.assertTrue(expected_result in results)
