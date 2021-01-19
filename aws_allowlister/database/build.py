import os
import requests
from bs4 import BeautifulSoup
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.scrapers.tables.standard import scrape_standard_table
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.scrapers.tables.iso import scrape_iso_table
from aws_allowlister.scrapers.tables.hipaa import scrape_hipaa_table
from aws_allowlister.database.database import DATABASE_PATH, connect_db, ComplianceTable


ALL_SERVICE_PREFIXES = get_all_service_prefixes()


def create_empty_compliance_database(db_session):
    for service_prefix in ALL_SERVICE_PREFIXES:
        name = get_service_prefix_data(service_prefix)["service_name"]
        db_session.add(
            ComplianceTable(
                service_prefix=service_prefix,
                name=name,
                alternative_names="",
                SOC="",
                PCI="",
                ISO="",
                FedRAMP="",
                HIPAA="",
                HITRUST="",
                IRAP="",
                OSPAR="",
                FINMA="",
            )
        )
        db_session.commit()


def build_compliance_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    db_session = connect_db()
    link = "https://aws.amazon.com/compliance/services-in-scope/"
    response = requests.get(link, allow_redirects=False)
    html_docs_destination = os.path.join(
        os.path.dirname(__file__), os.path.pardir, "data"
    )
    file_name = "services-in-scope.html"
    html_file_path = os.path.join(html_docs_destination, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)

    get_aws_html(link, html_docs_destination, file_name)

    def get_standard_names(this_soup):
        all_standard_names = []
        for li in this_soup.find_all("li"):
            if li.get("id"):
                if li.get("id").startswith("aws-element"):
                    all_standard_names.append(li.contents[1].text)
        return all_standard_names

    def get_table_ids(this_soup):
        table_ids = []
        for li in this_soup.find_all("li"):
            if li.get("id"):
                if li.get("id").startswith("aws-element"):
                    table_ids.append(li.get("id"))
        return table_ids

    with open(os.path.join(html_docs_destination, file_name), "r") as f:

        soup = BeautifulSoup(response.content, "html.parser")

        standard_names = get_standard_names(this_soup=soup)
        table_ids = get_table_ids(this_soup=soup)

        create_empty_compliance_database(db_session)

        these_results = []
        for this_table_id in table_ids:
            table = soup.find(id=this_table_id)

            # Get the standard name based on the "tab" name
            tab = table.contents[1]
            standard_name = tab.contents[0]

            # Skip certain cases based on inconsistent formatting
            exclusions = ["FedRAMP", "DoD CC SRG", "HIPAA BAA", "MTCS"]
            if standard_name in exclusions:
                continue
            rows = table.find_all("tr")
            if len(rows) == 0:
                continue

            # Scrape it
            result = scrape_standard_table(db_session, soup, this_table_id)
            these_results.append(result)
    scrape_iso_table(db_session)
    scrape_hipaa_table(db_session)
