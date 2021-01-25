import logging
import json
import click
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister import set_stream_logger
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
    '--quiet', '-q',
    is_flag=True,
    default=False,
)
def generate(all_standards, soc, pci, hipaa, iso, fedramp_high, fedramp_moderate, include, exclude, quiet):
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
    if (
        all_standards
        and not soc
        and not pci
        and not hipaa
        and not iso
        and not fedramp_high
        and not fedramp_moderate
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
    ):
        standards = ["SOC", "PCI", "HIPAA", "ISO", "FedRAMP_High", "FedRAMP_Moderate"]
        logger.info(f"--all was selected. The policy will include the default standard(s): {str(', '.join(standards))}")
    logger.info(f"Note: to silence these logs, supply the argument '--quiet'")
    logger.info(f"Policies for standard(s): {str(', '.join(standards))}")
    results = generate_allowlist_scp(standards, include, exclude)
    print(json.dumps(results, indent=4))


def generate_allowlist_scp(standards, include=None, exclude=None):
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
        allowed_services.append(f"{service}:*")

    policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Sid": "AllowList",
            "Effect": "Deny",
            "NotAction": allowed_services,
            "Resource": "*",
        },
    }
    return policy
