import logging
from aws_allowlister.database.database import RawScrapingDataTable
logger = logging.getLogger(__name__)


class RawScrapingData:
    def __init__(self):
        self.note = None

    def standards(self, db_session):
        query = db_session.query(
            RawScrapingDataTable.compliance_standard_name.distinct().label(
                "compliance_standard_name"
            )
        )
        standards = [row.compliance_standard_name for row in query.all()]
        return standards

    def get_rows(self, db_session, sdk_name=None, service_name=None, standard=None):
        if sdk_name:
            rows = db_session.query(RawScrapingDataTable).filter(
                RawScrapingDataTable.sdk_name == sdk_name
            )
        elif service_name:
            rows = db_session.query(RawScrapingDataTable).filter(
                RawScrapingDataTable.service_name == service_name
            )
        elif standard:
            rows = db_session.query(RawScrapingDataTable).filter(
                RawScrapingDataTable.compliance_standard_name == standard
            )
        else:
            rows = db_session.query(RawScrapingDataTable)
        size = len(rows.all())
        results = []
        for row in rows:
            res = row.__dict__
            res.pop("_sa_instance_state", None)
            res.pop("id", None)
            results.append(row.__dict__)
        return results

    def get_sdk_names_matching_compliance_standard(self, db_session, standard_name):
        """
        Get a list of all SDK names matching this compliance standard from the Scraping Table
        """
        rows = db_session.query(RawScrapingDataTable).filter(
            RawScrapingDataTable.compliance_standard_name == standard_name
        )
        sdk_names = {}
        for row in rows:
            sdk_names[row.sdk_name] = row.service_name
        return sdk_names

    def get_service_names_matching_compliance_standard(self, db_session, standard_name):
        """
        Get a list of all SDK names matching this compliance standard from the Scraping Table
        """
        rows = db_session.query(RawScrapingDataTable).filter(
            RawScrapingDataTable.compliance_standard_name == standard_name
        )
        service_names = {}
        for row in rows:
            service_names[row.service_name] = row.sdk_name
        return service_names

    def add_entry_to_database(self, db_session, compliance_standard_name, service_name, sdk):
        """Add an entry to the database"""
        db_session.add(
            RawScrapingDataTable(
                compliance_standard_name=compliance_standard_name,
                sdk_name=sdk,
                service_name=service_name,
            )
        )
        db_session.commit()
