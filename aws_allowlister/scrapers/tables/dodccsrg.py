import os
from bs4 import BeautifulSoup, Tag
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.aws_docs import get_aws_html
from aws_allowlister.shared.utils import chomp, chomp_keep_single_spaces
from aws_allowlister.scrapers.common import get_table_ids, clean_status_cell, clean_sdks, get_service_name, clean_status_cell_contents
from sqlalchemy.orm.session import Session

"""Almost the same as the standard table but with extra columns"""


def scrape_dodccsrg_table(db_session: Session, link: str, destination_folder: str, file_name: str, download: bool = True):
    html_file_path = os.path.join(destination_folder, file_name)

    if download:
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
        get_aws_html(link, html_file_path)

    raw_scraping_data = RawScrapingData()

    with open(html_file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        table_ids = get_table_ids(this_soup=soup)
        for this_table_id in table_ids:
            table = soup.find(id=this_table_id)

            # Get the standard name based on the "tab" name
            tab = table.contents[1]
            standard_name = chomp_keep_single_spaces(str(tab.contents[0]))
            # We are only scraping DoD CC SRG here
            if standard_name != "DoD CC SRG":
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
                # print(f"DoD CC SRG service_name: {this_service_name}")

                # Cell 1: DoD CC SRG IL2 (East/West)
                dodccsrg_il2_ew_status, fedramp_moderate_status_contents = clean_status_cell_contents(cells[1].contents[0])
                if dodccsrg_il2_ew_status:
                    # print(f"dodccsrg_il2_ew_status: {dodccsrg_il2_ew_status}, {dodccsrg_il2_ew_status_contents}")
                    raw_scraping_data.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name="DoDCCSRG_IL2_EW",
                        sdk="",
                        service_name=this_service_name,
                    )

                # Cell 2: DoD CC SRG IL2 (GovCloud)
                dodccsrg_il2_gc_status, dodccsrg_il2_gc_status_contents = clean_status_cell_contents(cells[2].contents[0])
                if dodccsrg_il2_gc_status:
                    # print(f"dodccsrg_il2_gc_status: {dodccsrg_il2_gc_status}, {dodccsrg_il2_gc_status_contents}")
                    raw_scraping_data.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name="DoDCCSRG_IL2_GC",
                        sdk="",
                        service_name=this_service_name,
                    )

                # Cell 3: DoD CC SRG IL4 (GovCloud)
                dodccsrg_il4_gc_status, dodccsrg_il4_gc_status_contents = clean_status_cell_contents(cells[3].contents[0])
                if dodccsrg_il4_gc_status:
                    # print(f"dodccsrg_il4_gc_status: {dodccsrg_il4_gc_status}, {dodccsrg_il4_gc_status_contents}")
                    raw_scraping_data.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name="DoDCCSRG_IL4_GC",
                        sdk="",
                        service_name=this_service_name,
                    )

                # Cell 4: DoD CC SRG IL5 (GovCloud)
                dodccsrg_il5_gc_status, dodccsrg_il5_gc_status_contents = clean_status_cell_contents(cells[4].contents[0])
                if dodccsrg_il5_gc_status:
                    # print(f"dodccsrg_il5_status: {dodccsrg_il5gc__status}, {dodccsrg_il5_gc_status_contents}")
                    raw_scraping_data.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name="DoDCCSRG_IL5_GC",
                        sdk="",
                        service_name=this_service_name,
                    )
