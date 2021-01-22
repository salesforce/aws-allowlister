import os
import requests
from bs4 import Tag, NavigableString, BeautifulSoup
from aws_allowlister.shared.utils import chomp, clean_service_name
# from aws_allowlister.database.scraping_data import add_scraping_entry_to_input_database
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.aws_docs import get_aws_html


def scrape_standard_table(db_session):
    results = []

    # Get the file
    html_docs_destination = os.path.join(
        os.path.dirname(__file__), os.path.pardir, os.path.pardir, "data"
    )
    file_name = "services-in-scope.html"
    html_file_path = os.path.join(html_docs_destination, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    # Start scraping the standard table
    link = "https://aws.amazon.com/compliance/services-in-scope/"
    file_path = get_aws_html(link, html_docs_destination, file_name)

    raw_scraping_data = RawScrapingData()

    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        table_ids = get_table_ids(this_soup=soup)

        # these_results = []
        for this_table_id in table_ids:
            table = soup.find(id=this_table_id)

            # Get the standard name based on the "tab" name
            tab = table.contents[1]
            standard_name = chomp(str(tab.contents[0]))
            print(f"Scraping table for {standard_name}")

            # Skip certain cases based on inconsistent formatting
            exclusions = ["FedRAMP", "DoD CC SRG", "HIPAA BAA", "MTCS"]
            if standard_name in exclusions:
                continue
            rows = table.find_all("tr")
            if len(rows) == 0:
                continue

            # Scrape it

            for row in rows:
                cells = row.find_all("td")
                # Skip the first row, the rest are the same
                if len(cells) == 0 or len(cells) == 1:
                    continue

                # Cell 0: Service name

                this_service_name = get_service_name(cells)

                # Cell 1: SDKs
                # For the HIPAA BAA compliance standard, there are only two columns 🙄 smh at inconsistency
                these_sdks = clean_sdks(cells)

                # Cell 2: Status cell
                # This will contain a checkmark (✓). Let's just mark as true if it is non-empty
                this_status, this_status_cell_contents = clean_status_cell(cells)

                result = dict(
                    service_name=this_service_name,
                    sdks=these_sdks,
                    status=this_status,
                    status_text=this_status_cell_contents,
                )
                for sdk in these_sdks:
                    raw_scraping_data.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name=standard_name,
                        sdk=sdk,
                        service_name=this_service_name,
                    )
                results.append(result)
    return results


def get_service_name(some_cells):
    service_name_cell = some_cells[0].contents[1]
    if isinstance(service_name_cell, NavigableString):
        service_name = str(service_name_cell)
    elif isinstance(service_name_cell, Tag):
        service_name = service_name_cell.text
    else:
        service_name = str(service_name_cell)
    service_name = clean_service_name(service_name)
    return service_name


def clean_sdks(some_cells):
    sdks = []
    if len(some_cells) < 3:
        pass
    # Otherwise,
    else:
        cell_content = chomp(some_cells[1].contents[0])
        if "<a" in cell_content or "]" in cell_content:
            cell_content = some_cells[1].contents[0].text
        if not cell_content:
            pass
        else:
            if "," in cell_content:
                tmp_sdk_list = cell_content.split(",")
                for tmp_sdk in tmp_sdk_list:
                    sdks.append(chomp(tmp_sdk))
            else:
                sdks = [cell_content]
    return sdks


def clean_status_cell(cells):
    # Slice syntax in case there are only two columns
    status_cell_contents = cells[-1].contents[0]

    if status_cell_contents is None:
        status = False
    elif isinstance(status_cell_contents, str):
        status_cell_contents = chomp(status_cell_contents)
    elif isinstance(status_cell_contents, Tag):
        status_cell_contents = chomp(status_cell_contents.text)
    elif isinstance(status_cell_contents, NavigableString):
        status_cell_contents = chomp(str(status_cell_contents))
    else:
        print("idk what type it is")

    if status_cell_contents is None:
        status = False
    elif "✓" in status_cell_contents:
        status = True
    elif status_cell_contents != "✓":
        status = False
    else:
        status = True

    return status, status_cell_contents


def get_table_ids(this_soup):
    table_ids = []
    for li in this_soup.find_all("li"):
        if li.get("id"):
            if li.get("id").startswith("aws-element"):
                table_ids.append(li.get("id"))
    return table_ids


def get_standard_names(this_soup):
    all_standard_names = []
    for li in this_soup.find_all("li"):
        if li.get("id"):
            if li.get("id").startswith("aws-element"):
                all_standard_names.append(li.contents[1].text)
    return all_standard_names
