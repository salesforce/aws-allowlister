import json
import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()

class ComplianceDataTestCase(unittest.TestCase):
    def test_get_standard_names(self):
        result = compliance_data.standard_names(db_session=db_session)
        # print(result)
        expected_result = ['SOC', 'PCI', 'ISO', 'FedRAMP', 'HIPAA', 'HITRUST', 'IRAP', 'OSPAR', 'FINMA']
        self.assertListEqual(result, expected_result)

    def test_get_compliance_status(self):
        # print("getting the status")
        status = compliance_data.get_compliance_status(
            db_session=db_session,
            service_prefix="account",
            compliance_standard="SOC"
        )
        print(status)
        self.assertEqual(status, True)

    def test_get_rows_matching_service_prefix(self):
        results = compliance_data.get_rows_matching_service_prefix(db_session=db_session, service_prefix="s3")
        print(json.dumps(results, indent=4))
        self.assertTrue(len(results) == 1)
        expected_result = [
            {
                "OSPAR": "",
                "IRAP": "",
                "HIPAA": "",
                "ISO": "",
                "SOC": "",
                "name": "Amazon S3",
                "FINMA": "",
                "HITRUST": "",
                "FedRAMP": "",
                "PCI": "",
                "alternative_names": "",
                "service_prefix": "s3"
            }
        ]
        self.assertTrue(len(results) == 1)
