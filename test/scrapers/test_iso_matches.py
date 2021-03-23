import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class IsoQATestCase(unittest.TestCase):
    def test_gh_09_ISO_compliant_services(self):
        results = compliance_data.get_compliant_services(
            db_session=db_session, compliance_standard="ISO"
        )
        expected_results = [
            "mobiletargeting",
            "macie",
            "kafka"
        ]
        print(results)
        # print(len(expected_results))
        for expected_result in expected_results:
            # print(expected_result)
            print(f"{expected_result} in {results}")
            self.assertTrue(expected_result in results)

        self.assertTrue("msk" not in results)
