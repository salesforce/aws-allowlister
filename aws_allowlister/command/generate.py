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
    required=False,
    is_flag=True,
    default=True,
    help="SOC, PCI, ISO, and HIPAA.",
)
@click.option(
    "--soc",
    "-s",
    required=False,
    is_flag=True,
    default=False,
    help="Include SOC-compliant policies",
)
@click.option(
    "--pci",
    "-p",
    required=False,
    is_flag=True,
    default=False,
    help="Include PCI-compliant policies",
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
    help="Include ISO-compliant policies",
)
@click.option(
    "--include",
    required=False,
    default=None,
    callback=validate_comma_separated_aws_services,
    help="Include specific AWS IAM services, specified in a comma separated string."
)
@click.option(
    "--exclude",
    required=False,
    default=None,
    callback=validate_comma_separated_aws_services,
    help="Exclude specific AWS IAM services, specified in a comma separated string."
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    default=False,
)
def generate(all, soc, pci, hipaa, iso, include, exclude, quiet):
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
    if (
        all
        and not soc
        and not pci
        and not hipaa
        and not iso
    ):
        standards = ["SOC", "PCI", "HIPAA", "ISO"]
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
    services = list(standard_results[0].intersection(*standard_results))
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
