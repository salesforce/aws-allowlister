import os
from bs4 import BeautifulSoup, Tag
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.shared.utils import clean_service_name


def scrape_iso_table(db_session, link, destination_folder, file_name):
    html_file_path = os.path.join(destination_folder, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)

    # get_aws_html gets the HTML from AWS docs and stores it locally, then returns the path
    get_aws_html(link, html_file_path)

    raw_scraping_data = RawScrapingData()

    with open(html_file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        table = soup.find("tbody")
        rows = []
        for row in table.contents:
            if isinstance(row, Tag):
                rows.append(row)

        for row in rows:
            if isinstance(row, Tag):
                service_name = clean_service_name(str(row.contents[1].text))
                sdk = clean_service_name(str(row.contents[3].text))
                if sdk == "Namespaces*" or service_name == "AWS Services":
                    continue
                raw_scraping_data.add_entry_to_database(
                    db_session=db_session,
                    compliance_standard_name="ISO",
                    sdk=sdk,
                    service_name=clean_service_name(service_name),
                )
