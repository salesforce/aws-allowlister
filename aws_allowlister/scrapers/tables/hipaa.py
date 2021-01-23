import os
import requests
from bs4 import BeautifulSoup
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.shared.utils import clean_service_name

ALL_SERVICE_PREFIXES = get_all_service_prefixes()


def scrape_hipaa_table(db_session):
    html_docs_destination = os.path.join(
        os.path.dirname(__file__), os.path.pardir, os.path.pardir, "data"
    )
    file_name = "hipaa-eligible-services-reference.html"
    html_file_path = os.path.join(html_docs_destination, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    link = "https://aws.amazon.com/compliance/hipaa-eligible-services-reference/"

    get_aws_html(link, html_docs_destination, file_name)
    response = requests.get(link, allow_redirects=False)
    # soup = BeautifulSoup(response.content, "html.parser")
    raw_scraping_data = RawScrapingData()

    service_names = []

    # These show up as list items but are not relevant at all
    false_positives = [
        "AWS Cloud Security",
        "AWS Solutions Portfolio",
        "AWS Partner Network",
        "AWS Careers",
        "AWS Support Overview",
    ]
    with open(os.path.join(html_docs_destination, file_name), "r") as f:
        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup.find_all("li"):
            if (
                tag.text.startswith("Amazon")
                or tag.text.startswith("AWS")
                or tag.text.startswith("Elastic")
                or tag.text.startswith("Alexa")
            ):
                if tag.text not in false_positives:
                    service_names.append(tag.text)
    for service_name in service_names:
        raw_scraping_data.add_entry_to_database(
            db_session=db_session,
            compliance_standard_name="HIPAA",
            sdk="",  # The HIPAA table does not list SDKs. We will update it to match in a second.
            service_name=clean_service_name(service_name),
        )
