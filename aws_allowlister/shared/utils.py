import os
import json
import re
import logging
import yaml
from bs4 import NavigableString, Tag
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.shared.iam_data import get_service_prefix_data, iam_definition


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
ALL_SERVICE_PREFIXES = get_all_service_prefixes()


def get_service_name_matching_iam_service_prefix(iam_service_prefix):
    if iam_definition.get(iam_service_prefix):
        service_name = get_service_prefix_data(iam_service_prefix)["service_name"]
        return service_name
    else:
        return None


def chomp(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", "")
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


def chomp_keep_single_spaces(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", " ")  # Replace weird spaces with regular spaces
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


# pylint: disable=inconsistent-return-statements
def normalize_tags_or_strings(val):
    if isinstance(val, str):
        result = chomp(val)
        return result
    # NavigableString will represent the final value we want
    elif isinstance(val, NavigableString):
        result = chomp(str(val))
        return result
    # If it's a tag, we need to run it through this again until we get to NavigableString
    elif isinstance(val, Tag):
        try:
            tmp = normalize_tags_or_strings(val.contents[-1])
            if len(tmp) > 0:
                processed = tmp
            else:
                tmp = normalize_tags_or_strings(val.contents[0])
                processed = str(tmp)
        except IndexError as i_e:
            print(i_e)
            processed = str(val.contents)
        return processed


def clean_service_name(service_name):
    # Remove non-breaking spaces, otherwise you will have service names like "AWS Amplify\u00a0",
    service_name = service_name.replace(u"\xa0", u" ")
    service_name = re.sub("\s\s+", " ", service_name)

    # # Remove all text after brackets [
    # #   Example: Amazon Aurora on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
    # service_name, sep, tail = service_name.partition("[")
    #
    # # Remove all text after parentheses (
    #   Example: Alexa for Business on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
    #   'Alexa for Business (for healthcare skills only – requires Alexa Skills BAA. See
    #   HIPAA whitepaper for details)'
    # service_name, sep, tail = service_name.partition("(")

    # Remove tabs and newlines
    service_name = service_name.replace('\n', '')
    service_name = service_name.replace('\t', '')
    # Clean start
    service_name = re.sub("^[ ]*", "", service_name)
    # Clean end
    service_name = re.sub("[ ]*$", "", service_name)
    return service_name


def clean_service_name_after_brackets_and_parentheses(service_name):
    try:
        # Remove all text after brackets [
        #   Example: Amazon Aurora on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
        #   'Amazon Aurora [MySQL, PostgreSQL]'
        service_name, sep, tail = service_name.partition("[")

        # Remove all text after parentheses (
        #   Example: Alexa for Business on https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
        #   'Alexa for Business (for healthcare skills only – requires Alexa Skills BAA. See HIPAA whitepaper for details)'
        service_name, sep, tail = service_name.partition("(")
        # Clean start
        service_name = re.sub("^[ ]*", "", service_name)
        # Clean end
        service_name = re.sub("[ ]*$", "", service_name)
        service_name = clean_service_name(service_name)
    except AttributeError as a_e:
        logger.debug(f"{a_e}: {service_name}")
        # Set it to a blank string so it doesn't break
        service_name = ""
    return service_name


def write_json_to_file(file_name, content):
    definition_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), file_name)
    )

    if os.path.exists(definition_file):
        os.remove(definition_file)

    with open(definition_file, "w") as file:
        json.dump(content, file, indent=4)


def read_yaml_file(filename):
    """
    Reads a YAML file, safe loads, and returns the dictionary

    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    return cfg
