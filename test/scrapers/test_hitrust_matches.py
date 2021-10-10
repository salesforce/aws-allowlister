import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class HitrustQATestCase(unittest.TestCase):
    def test_gh_20_HITRUST_compliant_services(self):
        results = compliance_data.get_compliant_services(
            db_session=db_session, compliance_standard="HITRUST"
        )
        expected_results = [
            "athena",
            "kendra",
            "guardduty",
            "sagemaker",
            "step-functions"
        ]
        # print(len(results))
        for expected_result in expected_results:
            # print(f"{expected_result}: in {expected_result in results}")
            self.assertTrue(expected_result in results)
