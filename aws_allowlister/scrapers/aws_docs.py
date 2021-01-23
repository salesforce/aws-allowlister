import logging
import os
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# TODO: Duplicate code passing in these parameters
def get_aws_html(link, file_path):
    """
    Get the AWS docs, modify the CSS paths so things display properly, save it locally, and return the path.
    """
    file_name = os.path.basename(file_path)

    print(f"Getting the AWS documentation for: {file_name}")

    response = requests.get(link, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")

    def cleanup_links():
        # Replace the CSS stuff. Basically this:
        """
        <link href='href="https://docs.aws.amazon.com/images/favicon.ico"' rel="icon" type="image/ico"/>
        <link href='href="https://docs.aws.amazon.com/images/favicon.ico"' rel="shortcut icon" type="image/ico"/>
        <link href='href="https://docs.aws.amazon.com/font/css/font-awesome.min.css"' rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/css/code/light.css"' id="code-style" rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/css/awsdocs.css?v=20181221"' rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/assets/marketing/css/marketing-target.css"' rel="stylesheet" type="text/css"/>
        list_amazonkendra.html downloaded
        """
        for link in soup.find_all("link"):
            if link.get("href").startswith("/"):
                temp = link.attrs["href"]
                link.attrs["href"] = link.attrs["href"].replace(
                    temp, f"https://docs.aws.amazon.com{temp}"
                )

        for script in soup.find_all("script"):
            try:
                if "src" in script.attrs:
                    if script.get("src").startswith("/"):
                        temp = script.attrs["src"]
                        script.attrs["src"] = script.attrs["src"].replace(
                            temp, f"https://docs.aws.amazon.com{temp}"
                        )
            except TypeError as t_e:
                logger.warning(t_e)
                logger.warning(script)
            except AttributeError as a_e:
                logger.warning(a_e)
                logger.warning(script)

    cleanup_links()

    # file_path = os.path.join(html_docs_destination, file_name)
    if os.path.exists(file_path):
        print(f"Removing old file path: {file_path}")
        os.remove(file_path)
    with open(file_path, "w") as file:
        print(f"Creating new file: {os.path.abspath(file_path)}")
        file.write(str(soup.prettify()))
        file.close()
    logger.info("%s downloaded", file_name)
    return file_path
