import json
import click
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import ComplianceData


@click.command(
    name="generate",
    short_help="Generate an AWS AllowList policy based on compliance requirements",
)
@click.option(
    "--soc",
    "-s",
    required=False,
    is_flag=True,
    default=True,
    help="Include SOC-compliant policies",
)
@click.option(
    "--pci",
    "-p",
    required=False,
    is_flag=True,
    default=True,
    help="Include PCI-compliant policies",
)
@click.option(
    "--hipaa",
    "-h",
    required=False,
    is_flag=True,
    default=True,
    help="Include HIPAA-compliant services",
)
@click.option(
    "--iso",
    "-i",
    required=False,
    is_flag=True,
    default=True,
    help="Include ISO-compliant policies",
)
def generate(soc, pci, hipaa, iso):
    standards = []
    if soc:
        standards.append("SOC")
    if pci:
        standards.append("PCI")
    if hipaa:
        standards.append("HIPAA")
    if iso:
        standards.append("ISO")
    results = generate_allowlist_scp(standards)
    print(json.dumps(results, indent=4))


def generate_allowlist_scp(standards):
    db_session = connect_db()
    compliance_data = ComplianceData()
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
    services.sort()
    allowed_services = []
    for service in services:
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
