from bs4 import Tag, NavigableString, BeautifulSoup
from aws_allowlister.shared.utils import chomp, clean_service_name


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
    status, status_cell_contents = clean_status_cell_contents(status_cell_contents)
    # if status_cell_contents is None:
    #     status = False
    # elif isinstance(status_cell_contents, str):
    #     status_cell_contents = chomp(status_cell_contents)
    # elif isinstance(status_cell_contents, Tag):
    #     status_cell_contents = chomp(status_cell_contents.text)
    # elif isinstance(status_cell_contents, NavigableString):
    #     status_cell_contents = chomp(str(status_cell_contents))
    # else:
    #     print("idk what type it is")
    #
    # if status_cell_contents is None:
    #     status = False
    # elif "✓" in status_cell_contents:
    #     status = True
    # elif status_cell_contents != "✓":
    #     status = False
    # else:
    #     status = True

    return status, status_cell_contents


def clean_status_cell_contents(status_cell_contents):
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
