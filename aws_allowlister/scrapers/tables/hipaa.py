import os
import requests
from bs4 import BeautifulSoup
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.shared.utils import clean_service_name

ALL_SERVICE_PREFIXES = get_all_service_prefixes()


def scrape_hipaa_table(db_session, link, destination_folder, file_name):
    html_file_path = os.path.join(destination_folder, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)

    # get_aws_html gets the HTML from AWS docs and stores it locally, then returns the path
    get_aws_html(link, html_file_path)

    raw_scraping_data = RawScrapingData()

    # These show up as list items but are not relevant at all
    false_positives = [
        "AWS Cloud Security",
        "AWS Management Console"
        "AWS CloudEndure"
        "Amazon CloudWatch SDK Metrics"
        "AWS Managed Services",
        "AWS Solutions Portfolio",
        "AWS Partner Network",
        "AWS Careers",
        "AWS Support Overview",
    ]
    service_names = []
    with open(html_file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.find_all("li"):
            cleaned = clean_service_name(tag.text)
            if (
                cleaned.startswith("Amazon")
                or cleaned.startswith("AWS")
                or cleaned.startswith("Elastic")
                or cleaned.startswith("Alexa")
            ):
                if cleaned not in false_positives:
                    service_names.append(cleaned)

    for service_name in service_names:
        raw_scraping_data.add_entry_to_database(
            db_session=db_session,
            compliance_standard_name="HIPAA",
            sdk="",  # The HIPAA table does not list SDKs. We will update it to match in a second.
            service_name=clean_service_name(service_name),
        )
