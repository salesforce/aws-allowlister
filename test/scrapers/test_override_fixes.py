import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


class OverridesQualityChecksTestCase(unittest.TestCase):
    """Some contributors suggest changes to the overrides, per service or per framework.
    These test cases are meant to verify the targeted changes work as intended."""
    def test_gh_48_ec2messages_ssmmessages(self):
        standards = ["SOC", "PCI", "ISO", "FedRAMP_High", "FedRAMP_Moderate", "HIPAA", "IRAP", "OSPAR", "FINMA"]
        for standard in standards:
            results = compliance_data.get_compliant_services(
                db_session=db_session, compliance_standard=standard
            )
            for expected_result in ["ssm", "ssmmessages", "ec2messages"]:
                print(f"Checking if {standard} allows {expected_result}")
                self.assertTrue(expected_result in results)
