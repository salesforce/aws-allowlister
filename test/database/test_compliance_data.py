import json
import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class ComplianceDataTestCase(unittest.TestCase):
    def test_standard_names(self):
        """database.scrapers.compliance_data.ComplianceData.standard_names"""
        results = compliance_data.standard_names(db_session=db_session)
        # print(result)
        expected_results = ['SOC', 'PCI', 'ISO', 'FedRAMP', 'HIPAA', 'HITRUST', 'IRAP', 'OSPAR', 'FINMA']
        self.assertListEqual(results, expected_results)

    def test_get_rows(self):
        """database.scrapers.compliance_data.ComplianceData.get_rows"""
        results = compliance_data.get_rows(db_session=db_session, service_prefix="s3")
        print(len(results))
        print(json.dumps(results, indent=4))
        expected_results = [
            {
                "OSPAR": "true",
                "IRAP": "true",
                "HIPAA": "true",
                "ISO": "true",
                "SOC": "true",
                "name": "Amazon S3",
                "FINMA": "true",
                "HITRUST": "",
                "FedRAMP": "",
                "PCI": "true",
                "service_prefix": "s3"
            }
        ]

    def test_get_compliance_status(self):
        """database.scrapers.compliance_data.ComplianceData.get_compliance_status"""
        # print("getting the status")
        status = compliance_data.get_compliance_status(
            db_session=db_session,
            service_prefix="account",
            compliance_standard="SOC"
        )
        print(status)
        self.assertEqual(status, True)

    def test_get_rows_matching_service_prefix(self):
        """database.scrapers.compliance_data.ComplianceData.get_rows_matching_service_prefix"""
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
                "service_prefix": "s3"
            }
        ]
        self.assertTrue(len(results) == 1)

    def test_get_compliant_services(self):
        """database.scrapers.compliance_data.ComplianceData.get_compliant_services"""
        results = compliance_data.get_compliant_services(db_session=db_session, compliance_standard="SOC")
