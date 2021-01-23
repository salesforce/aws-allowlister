import logging
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.database.database import ComplianceTable
from aws_allowlister.database.transformed_scraping_data import TransformedScrapingData
from aws_allowlister.scrapers.overrides import Overrides
from aws_allowlister.shared.utils import get_service_name_matching_iam_service_prefix

ALL_SERVICE_PREFIXES = get_all_service_prefixes()
logger = logging.getLogger(__name__)


class ComplianceData:
    def __init__(self):
        self.note = None

    def standard_names(self, db_session):
        """Get the names of the standards mentioned in the Compliance Database table"""
        standard_names = ComplianceTable.metadata.tables[
            "compliancetable"
        ].columns.keys()
        for item in ["id", "service_prefix", "name"]:
            standard_names.remove(item)
        db_session.close()
        return standard_names

    def get_rows(self, db_session, service_prefix=None, service_name=None):
        """Get rows as a list of dictionaries"""
        if service_prefix:
            rows = db_session.query(ComplianceTable).filter(
                ComplianceTable.service_prefix == service_prefix
            )
        elif service_name:
            rows = db_session.query(ComplianceTable).filter(
                ComplianceTable.name == service_name
            )
        else:
            rows = db_session.query(ComplianceTable)
        size = len(rows.all())
        results = []
        for row in rows:
            res = row.__dict__
            res.pop("_sa_instance_state", None)
            res.pop("id", None)
            results.append(row.__dict__)
        return results

    def update_compliance_status(
        self, db_session, service_prefix, compliance_standard, status
    ):
        """
        update compliancetable
        set SOC = "false"
        where service_prefix = "a4b";
        """
        rows = db_session.query(ComplianceTable).filter(
            ComplianceTable.service_prefix == service_prefix
        )
        size = len(rows.all())
        rows.update({compliance_standard: status})
        db_session.commit()
        db_session.close()
        return size

    def add_entry_to_database(self, db_session, service_prefix, name, standard):
        """Add an entry to the database"""
        # Let's add the empty entry to the database, then commit it,
        # then call the other function to update the actual status
        db_session.add(
            ComplianceTable(
                service_prefix=service_prefix,
                name=name,
                SOC="",
                PCI="",
                ISO="",
                FedRAMP_High="",
                FedRAMP_Moderate="",
                HIPAA="",
                HITRUST="",
                IRAP="",
                OSPAR="",
                FINMA="",
            )
        )
        db_session.commit()
        self.update_compliance_status(
            db_session=db_session,
            service_prefix=service_prefix,
            compliance_standard=standard,
            status="true"
        )

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
        # We set the database value to "true" or an empty string to avoid annoying SQLite errors
        return bool(status == "true")

    def get_rows_matching_service_prefix(self, db_session, service_prefix):
        """Get rows matching a given prefix and standard"""
        rows = db_session.query(ComplianceTable).filter(
            ComplianceTable.service_prefix == service_prefix
        )
        size = len(rows.all())
        results = []
        for row in rows:
            res = row.__dict__
            res.pop("_sa_instance_state", None)
            res.pop("id", None)
            results.append(row.__dict__)
        return results

    def service_prefixes(self, db_session):
        """Get a list of all unique service prefixes"""
        rows = self.get_rows(db_session=db_session)
        service_prefixes = list(set(map(lambda x: x.get("service_prefix"), rows)))
        service_prefixes.sort()
        return service_prefixes

    def get_compliant_services(self, db_session, compliance_standard):
        """Get a list of services compliant with a standard like ISO or SOC"""
        compliant_services = []
        for service_prefix in self.service_prefixes(db_session=db_session):
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
        all_service_prefixes = self.service_prefixes(db_session=db_session)
        for standard in self.standard_names(db_session):
            sdk_names = transformed_scraping_database.get_sdk_names_matching_compliance_standard(
                db_session, standard
            )

            # all_service_prefixes = get_all_service_prefixes()
            for service_prefix in all_service_prefixes:
                # If it matches the service prefix,
                #   update the compliance table (which has it sorted by IAM names) to check the box
                if service_prefix in list(sdk_names.keys()):
                    self.update_compliance_status(
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
                    self.update_compliance_status(
                        db_session=db_session,
                        service_prefix=iam_service_prefix,  # this is the IAM prefix
                        compliance_standard=standard,
                        status="true",
                    )

    def apply_overrides_for_direct_inserts_per_framework(self, db_session, overrides=None):
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")

        print("\nOVERRIDES: SECTION 4: Direct inserts, per framework")
        for standard in self.standard_names(db_session):
            # If 'SOC' exists under 'direct_inserts'
            service_keys = overrides.direct_inserts.get(standard)
            # If there are any services listed under that compliance standard
            if service_keys:
                # Then loop through it
                for service in service_keys:
                    current_rows = self.get_rows(
                        db_session=db_session,
                        service_prefix=service,
                    )
                    # Let's try to get the service name if possible to keep it clean.
                    service_name = get_service_name_matching_iam_service_prefix(service)
                    if not service_name:
                        service_name = ""
                    # This executes if there is no entry at all
                    if not current_rows:
                        print(f"direct_inserts: service={service}, standard={standard}")
                        self.add_entry_to_database(
                            db_session=db_session,
                            service_prefix=service,
                            standard=standard,
                            name=service_name
                        )
                    # This executes if the entry exists but we need to change it
                    else:
                        print(f"direct_inserts: service={service}, standard={standard}")
                        self.update_compliance_status(
                            db_session=db_session,
                            service_prefix=service,
                            compliance_standard=standard,
                            status="true"
                        )

    def apply_overrides_for_direct_removals_per_framework(self, db_session, overrides=None):
        print("\nOVERRIDES: SECTION 5: Direct removals, per framework")

        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")

        for standard in self.standard_names(db_session):
            # If 'SOC' exists under 'direct_removals'
            service_keys = overrides.direct_removals.get(standard)
            # If there are any services listed under that compliance standard
            if service_keys:
                # Then loop through it
                for service in service_keys:
                    rows_removed = self.update_compliance_status(
                        db_session=db_session,
                        compliance_standard=standard,
                        service_prefix=service,
                        status=""
                    )
                    print(f"direct_removals: service={service}, standard={standard}; removed {rows_removed}")

    def update_compliance_database(self, db_session, overrides=None):
        """Populate the compliance database, which we use for writing our SCPs, with the data from
        the TransformedScrapingData and some overrides magic."""
        if not overrides:
            overrides = Overrides()
        transformed_scraping_database = TransformedScrapingData()
        transformed_scraping_database.populate_table(db_session, overrides)
        self.update_database_by_matching_sdk_names_with_iam_prefixes(
            db_session=db_session, transformed_scraping_database=transformed_scraping_database
        )
        self.update_database_by_matching_compliance_names_with_iam_names(
            db_session=db_session, transformed_scraping_database=transformed_scraping_database
        )
        self.apply_overrides_for_direct_inserts_per_framework(db_session=db_session, overrides=overrides)
        self.apply_overrides_for_direct_removals_per_framework(db_session=db_session, overrides=overrides)
