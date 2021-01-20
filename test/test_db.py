import unittest
from aws_allowlister.database.compliance_data import ComplianceData, ScrapingData
from aws_allowlister.database.build import build_database
from aws_allowlister.database.database import connect_db, TransformedScrapingDataTable
from aws_allowlister.shared.utils import write_json_to_file
from policy_sentry.shared.iam_data import get_service_prefix_data


class DatabaseTestCase(unittest.TestCase):
    def test_get_standard_names(self):
        compliance_data = ComplianceData()
        db_session = connect_db()
        result = compliance_data.standard_names(db_session=db_session)
        print(result)
        expected_result = ['SOC', 'PCI', 'ISO', 'FedRAMP', 'HIPAA', 'HITRUST', 'IRAP', 'OSPAR', 'FINMA']
        self.assertListEqual(result, expected_result)

    def test_get_compliance_status(self):
        compliance_data = ComplianceData()
        db_session = connect_db()
        print("getting the status")
        status = compliance_data.get_compliance_status(
            db_session=db_session,
            service_prefix="account",
            compliance_standard="SOC"
        )
        print(status)
        self.assertEqual(status, "true")
