from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.database.database import ComplianceTable
from aws_allowlister.database.transformed_scraping_data import TransformedScrapingData
from aws_allowlister.scrapers.overrides import Overrides

ALL_SERVICE_PREFIXES = get_all_service_prefixes()


class ComplianceData:
    def __init__(self):
        self.note = None

    def standard_names(self, db_session):
        """Get the names of the standards mentioned in the Compliance Database table"""
        standard_names = ComplianceTable.metadata.tables[
            "compliancetable"
        ].columns.keys()
        for item in ["id", "service_prefix", "name", "alternative_names"]:
            standard_names.remove(item)
        db_session.close()
        return standard_names

    def set_compliance_status(
        self, db_session, service_prefix, compliance_standard, status
    ):
        """
        update compliancetable
        set SOC = "false"
        where service_prefix = "a4b";
        """
        row = db_session.query(ComplianceTable).filter(
            ComplianceTable.service_prefix == service_prefix
        )
        row.update({compliance_standard: status})
        db_session.commit()
        db_session.close()

    def get_compliance_status(self, db_session, service_prefix, compliance_standard):
        """Given a compliance standard name and the service prefix, get the true/false compliance status"""
        rows = db_session.query(ComplianceTable).filter(
            ComplianceTable.service_prefix == service_prefix
        )
        result_row = {}
        for row in rows:
            this_row = row.__dict__
            if compliance_standard in this_row:
                result_row = row.__dict__
                break
        status = result_row.get(compliance_standard)
        db_session.close()
        return status

    def get_compliant_services(self, db_session, compliance_standard):
        """Get a list of services compliant with a standard like ISO or SOC"""
        compliant_services = []
        for service_prefix in ALL_SERVICE_PREFIXES:
            rows = db_session.query(ComplianceTable).filter(
                ComplianceTable.service_prefix == service_prefix
            )
            result_row = {}
            for row in rows:
                this_row = row.__dict__
                if compliance_standard in this_row:
                    result_row = row.__dict__
                    break
            status = result_row.get(compliance_standard)
            if status == "true":
                compliant_services.append(service_prefix)
        db_session.close()
        return compliant_services

    def update_database_by_matching_sdk_names_with_iam_prefixes(self, db_session, transformed_scraping_database):
        """
        SDK names (the names listed on the compliance pages) and IAM service prefix do not match directly,
        so let's update the Compliance database table with the IAM names
        """
        for standard in self.standard_names(db_session):
            sdk_names = transformed_scraping_database.get_sdk_names_matching_compliance_standard(
                db_session, standard
            )

            all_service_prefixes = get_all_service_prefixes()
            for service_prefix in all_service_prefixes:
                # If it matches the service prefix,
                #   update the compliance table (which has it sorted by IAM names) to check the box
                if service_prefix in list(sdk_names.keys()):
                    self.set_compliance_status(
                        db_session=db_session,
                        service_prefix=service_prefix,
                        compliance_standard=standard,
                        status="true",
                    )

    def update_database_by_matching_compliance_names_with_iam_names(self, db_session, transformed_scraping_database):
        """
        The names of AWS services in the compliance pages vary; let's change the names of those services to directly
        match the names of the services as listed on the AWS IAM pages.
        """
        for standard in self.standard_names(db_session):

            # The service name in IAM-land
            iam_service_names = {}
            for service_prefix in ALL_SERVICE_PREFIXES:
                iam_service_names[service_prefix] = get_service_prefix_data(service_prefix)[
                    "service_name"
                ]

            # The service name in compliance land
            compliance_service_names = (
                transformed_scraping_database.get_service_names_matching_compliance_standard(
                    db_session, standard
                )
            )
            for iam_service_prefix in list(iam_service_names.keys()):
                iam_name = iam_service_names[iam_service_prefix]
                compliance_names = list(compliance_service_names.keys())
                if iam_name in compliance_names:
                    self.set_compliance_status(
                        db_session=db_session,
                        service_prefix=iam_service_prefix,  # this is the IAM prefix
                        compliance_standard=standard,
                        status="true",
                    )

    def update_compliance_database(self, db_session, overrides=None):
        """Populate the compliance database, which we use for writing our SCPs, with the data from
        the TransformedScrapingData and some overrides magic."""
        if not overrides:
            overrides = Overrides()
        transformed_scraping_database = TransformedScrapingData()
        transformed_scraping_database.populate_table(db_session, overrides)
        transformed_scraping_database.apply_overrides(db_session=db_session, overrides=overrides)
        self.update_database_by_matching_sdk_names_with_iam_prefixes(
            db_session=db_session, transformed_scraping_database=transformed_scraping_database
        )
        self.update_database_by_matching_compliance_names_with_iam_names(
            db_session=db_session, transformed_scraping_database=transformed_scraping_database
        )
