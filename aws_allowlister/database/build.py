import os
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.database.database import DATABASE_PATH, connect_db, ComplianceTable
from aws_allowlister.scrapers.tables.standard import scrape_standard_table
from aws_allowlister.scrapers.tables.iso import scrape_iso_table
from aws_allowlister.scrapers.tables.hipaa import scrape_hipaa_table
from aws_allowlister.scrapers.tables.fedramp import scrape_fedramp_table


ALL_SERVICE_PREFIXES = get_all_service_prefixes()


def create_empty_compliance_database(db_session):
    """
    Fill in the compliance database table with the service prefix (ex: s3)
        and the Service name (Simple Storage Service) and set all the values to blank strings
    """
    for service_prefix in ALL_SERVICE_PREFIXES:
        name = get_service_prefix_data(service_prefix)["service_name"]
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


def build_database():
    """Builds the database from AWS Documentation files from scratch."""
    # Remove previous database file and connect
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    db_session = connect_db()

    # First, fill in the compliance database table with the service prefix
    #   (ex: s3) and the Service name (Simple Storage Service) and set all the values to blank strings
    create_empty_compliance_database(db_session)

    html_docs_folder = os.path.join(os.path.dirname(__file__), os.path.pardir, "data")

    # Scrape the tables that follow the standard format.
    #   These compliance frameworks, and services that are certified by them, are located at:
    #       https://aws.amazon.com/compliance/services-in-scope/
    scrape_standard_table(
        db_session=db_session,
        link="https://aws.amazon.com/compliance/services-in-scope/",
        destination_folder=html_docs_folder,
        file_name="services-in-scope.html"
    )

    # ISO docs follow a different format.
    #   ISO compliant services are located at https://aws.amazon.com/compliance/iso-certified/
    scrape_iso_table(
        db_session=db_session,
        link="https://aws.amazon.com/compliance/iso-certified/",
        destination_folder=html_docs_folder,
        file_name="iso-certified.html"
    )

    # HIPAA Docs follow a different format.
    #   HIPAA compliant services are located at https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
    scrape_hipaa_table(
        db_session=db_session,
        link="https://aws.amazon.com/compliance/hipaa-eligible-services-reference/",
        destination_folder=html_docs_folder,
        file_name="hipaa-eligible-services-reference.html"
    )

    # FedRAMP Docs have a few extra columns
    #   They are located at the same as the standard ones, but we just have to treat them a bit differently.
    scrape_fedramp_table(
        db_session=db_session,
        link="https://aws.amazon.com/compliance/services-in-scope/",
        destination_folder=html_docs_folder,
        file_name="services-in-scope.html"
    )
