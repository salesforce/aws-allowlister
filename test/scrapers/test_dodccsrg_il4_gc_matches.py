import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class DoDCCSRGIL4GCQATestCase(unittest.TestCase):
    def test_gh_13_DoDCCRG_IL4_GC_compliant_services(self):
        results = compliance_data.get_compliant_services(
            db_session=db_session, compliance_standard="DoDCCSRG_IL4_GC"
        )
        expected_results = [
            "config",
            "datasync",
            "directconnect"
        ]
        # print(len(expected_results))
        for expected_result in expected_results:
            # print(expected_result)
            # print(f"{expected_result} in {results}")
            self.assertTrue(expected_result in results)

        # self.assertTrue("batch" not in results)
