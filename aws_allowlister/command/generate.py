import logging
import json
import click
from tabulate import tabulate
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister import set_stream_logger
from aws_allowlister.shared import utils
from policy_sentry.querying.all import get_service_authorization_url
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def validate_comma_separated_aws_services(ctx, param, value):
    if value is not None:
        try:
            include_services = value.split(",")
            return include_services
        except ValueError:
            raise click.BadParameter('Supply the AWS services in a comma separated string.')


@click.command(
    name="generate",
    short_help="Generate an AWS AllowList policy based on compliance requirements",
)
@click.option(
    "--all",
    "-a",
    'all_standards',
    required=False,
    is_flag=True,
    default=True,
    help="SOC, PCI, ISO, HIPAA, FedRAMP_High, and FedRAMP_Moderate.",
)
@click.option(
    "--soc",
    "-s",
    required=False,
    is_flag=True,
    default=False,
    help="Include SOC-compliant services",
)
@click.option(
    "--pci",
    "-p",
    required=False,
    is_flag=True,
    default=False,
    help="Include PCI-compliant services",
)
@click.option(
    "--hipaa",
    "-h",
    required=False,
    is_flag=True,
    default=False,
    help="Include HIPAA-compliant services",
)
@click.option(
    "--iso",
    "-i",
    required=False,
    is_flag=True,
    default=False,
    help="Include ISO-compliant services",
)
@click.option(
    "--fedramp-high",
    "-fh",
    required=False,
    is_flag=True,
    default=False,
    help="Include FedRAMP High",
)
@click.option(
    "--fedramp-moderate",
    "-fm",
    required=False,
    is_flag=True,
    default=False,
    help="Include FedRAMP Moderate",
)
@click.option(
    "--dodccsrg-il2-ew",
    "-d2e",
    required=False,
    is_flag=True,
    default=False,
    help="Include DoD CC SRG IL2 (East/West)",
)
@click.option(
    "--dodccsrg-il2-gc",
    "-d2g",
    required=False,
    is_flag=True,
    default=False,
    help="Include DoD CC SRG IL2 (GovCloud)",
)
@click.option(
    "--dodccsrg-il4-gc",
    "-d4g",
    required=False,
    is_flag=True,
    default=False,
    help="Include DoD CC SRG IL4 (GovCloud)",
)
@click.option(
    "--dodccsrg-il5-gc",
    "-d5g",
    required=False,
    is_flag=True,
    default=False,
    help="Include DoD CC SRG IL5 (GovCloud)",
)
@click.option(
    "--include",
    required=False,
    default=None,
    type=str,
    callback=validate_comma_separated_aws_services,
    help="Include specific AWS IAM services, specified in a comma separated string."
)
@click.option(
    "--exclude",
    required=False,
    type=str,
    default=None,
    callback=validate_comma_separated_aws_services,
    help="Exclude specific AWS IAM services, specified in a comma separated string."
)
@click.option(
    "--table",
    required=False,
    type=bool,
    default=False,
    is_flag=True,
    help="Instead of providing the output as JSON, output a markdown-formatted table of the Service Prefixes alongside Service Names."
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    default=False,
)
def generate(all_standards, soc, pci, hipaa, iso, fedramp_high, fedramp_moderate, 
             dodccsrg_il2_ew, dodccsrg_il2_gc, dodccsrg_il4_gc, dodccsrg_il5_gc, include, exclude, table, quiet):
    standards = []
    if quiet:
        log_level = getattr(logging, "WARNING")
        set_stream_logger(level=log_level)
    else:
        log_level = getattr(logging, "INFO")
        set_stream_logger(level=log_level)
    if soc:
        standards.append("SOC")
    if pci:
        standards.append("PCI")
    if hipaa:
        standards.append("HIPAA")
    if iso:
        standards.append("ISO")
    if fedramp_high:
        standards.append("FedRAMP_High")
    if fedramp_moderate:
        standards.append("FedRAMP_Moderate")
    if dodccsrg_il2_ew:
        standards.append("DoDCCSRG_IL2_EW")
    if dodccsrg_il2_gc:
        standards.append("DoDCCSRG_IL2_GC")
    if dodccsrg_il4_gc:
        standards.append("DoDCCSRG_IL4_GC")
    if dodccsrg_il5_gc:
        standards.append("DoDCCSRG_IL5_GC")
    if (
        all_standards
        and not soc
        and not pci
        and not hipaa
        and not iso
        and not fedramp_high
        and not fedramp_moderate
        and not dodccsrg_il2_ew
        and not dodccsrg_il2_gc
        and not dodccsrg_il4_gc
        and not dodccsrg_il5_gc
    ):
        standards = ["SOC", "PCI", "HIPAA", "ISO", "FedRAMP_High", "FedRAMP_Moderate"]
        logger.info(f"--all was selected. The policy will include the default standard(s): {str(', '.join(standards))}")
    if (
        not all_standards
        and not soc
        and not pci
        and not hipaa
        and not iso
        and not fedramp_high
        and not fedramp_moderate
        and not dodccsrg_il2_ew
        and not dodccsrg_il2_gc
        and not dodccsrg_il4_gc
        and not dodccsrg_il5_gc
    ):
        standards = ["SOC", "PCI", "HIPAA", "ISO", "FedRAMP_High", "FedRAMP_Moderate"]
        logger.info(f"--all was selected. The policy will include the default standard(s): {str(', '.join(standards))}")
    logger.info(f"Note: to silence these logs, supply the argument '--quiet'")
    logger.info(f"Policies for standard(s): {str(', '.join(standards))}")

    # If --table is provided, print as Markdown table. Otherwise, print the JSON policy
    if table:
        services = generate_allowlist_service_prefixes(standards, include, exclude)
        services_tabulated = []
        headers = ["Service Prefix", "Service Name"]
        # services_tabulated.append(headers)
        for service_prefix in services:
            service_name = utils.get_service_name_matching_iam_service_prefix(service_prefix)
            service_authorization_url = get_service_authorization_url(service_prefix)
            service_name_text = f"[{service_name}]({service_authorization_url})"
            # services_tabulated.append([service_prefix, service_name])
            services_tabulated.append([service_prefix, service_name_text])
        print(tabulate(services_tabulated, headers=headers, tablefmt="github"))
    else:
        results = generate_allowlist_scp(standards, include, exclude)

        minified_results = f"""{{
    "Version": "2012-10-17",
        "Statement": {{
            "Sid": "AllowList",
            "Effect": "Deny",
            "Resource": "*",
            "NotAction": {json.dumps(results.get('Statement').get('NotAction'))}
        }}
}}"""
        print(minified_results)
        # print(json.dumps(results, indent=4))


def generate_allowlist_scp(standards, include=None, exclude=None):
    """Get the SCP Policy document"""
    allowed_services = generate_allowlist_service_prefixes(standards=standards, include=include, exclude=exclude)
    allowed_services = format_allowlist_services(allowed_services)
    policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Sid": "AllowList",
            "Effect": "Deny",
            "Resource": "*",
            "NotAction": allowed_services
        },
    }
    return policy


def format_allowlist_services(services):
    result = ["{}{}".format(i, ":*") for i in services]
    return result


def generate_allowlist_service_prefixes(standards, include=None, exclude=None):
    """Generate a list of service Prefixes"""
    db_session = connect_db()
    compliance_data = ComplianceData()
    # This is a list of sets
    standard_results = []
    for standard in standards:
        standard_results.append(
            set(
                compliance_data.get_compliant_services(
                    db_session=db_session, compliance_standard=standard
                )
            )
        )
    # Intersect a collection of sets
    if len(standard_results) > 1:
        services = list(standard_results[0].intersection(*standard_results))
    else:
        services = list(standard_results[0])
    # Add the force-include services
    if include:
        services.extend(include)

    services.sort()

    allowed_services = []
    for service in services:
        # Remove the services that were specified for exclusion
        if exclude:
            if service in exclude:
                logger.info(f"{service} has been excluded from the policy")
                continue
        # If the service is not excluded, proceed
        allowed_services.append(service)
        # allowed_services.append(f"{service}:*")
    return allowed_services
