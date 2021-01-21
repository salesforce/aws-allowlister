import os
import requests
from bs4 import BeautifulSoup, Tag
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.shared.utils import clean_service_name


def scrape_iso_table(db_session):
    html_docs_destination = os.path.join(
        os.path.dirname(__file__), os.path.pardir, os.path.pardir, "data"
    )
    file_name = "iso-certified.html"
    html_file_path = os.path.join(html_docs_destination, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    link = "https://aws.amazon.com/compliance/iso-certified/"
    get_aws_html(link, html_docs_destination, file_name)
    response = requests.get(link, allow_redirects=False)

    raw_scraping_data = RawScrapingData()

    with open(html_file_path, "r") as f:
        # soup = BeautifulSoup(f.read(), "html.parser")
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("tbody")
        rows = []
        for row in table.contents:
            if isinstance(row, Tag):
                rows.append(row)

        for row in rows:
            if isinstance(row, Tag):
                service_name = str(row.contents[1].text)
                sdk = str(row.contents[3].text)
                if sdk == "Namespaces*" or service_name == "AWS Services":
                    continue
                raw_scraping_data.add_entry_to_database(
                    db_session=db_session,
                    compliance_standard_name="ISO",
                    sdk=sdk,
                    service_name=clean_service_name(service_name),
                )
