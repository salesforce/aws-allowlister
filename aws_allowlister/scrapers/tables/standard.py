import os
from bs4 import BeautifulSoup
from aws_allowlister.shared.utils import chomp, chomp_keep_single_spaces
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.scrapers.common import get_table_ids, clean_status_cell, clean_sdks, get_service_name


def scrape_standard_table(db_session, link, destination_folder, file_name):
    results = []

    html_file_path = os.path.join(destination_folder, file_name)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)

    # Start scraping the standard table
    get_aws_html(link, html_file_path)

    raw_scraping_data = RawScrapingData()

    with open(html_file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        table_ids = get_table_ids(this_soup=soup)

        # these_results = []
        for this_table_id in table_ids:
            table = soup.find(id=this_table_id)

            # Get the standard name based on the "tab" name
            tab = table.contents[1]
            standard_name = chomp_keep_single_spaces(str(tab.contents[0]))

            # Skip certain cases based on inconsistent formatting
            exclusions = ["FedRAMP", "DoD CC SRG", "HIPAA BAA", "MTCS"]
            if standard_name in exclusions:
                continue

            print(f"Scraping table for {standard_name}")
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
