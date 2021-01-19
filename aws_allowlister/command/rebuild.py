import click
from aws_allowlister.database.build import build_compliance_database
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import (
    ComplianceData,
    update_compliance_database,
)


@click.command(name="rebuild", short_help="Rebuild the database")
def rebuild():
    db_session = connect_db()
    build_compliance_database()
    update_compliance_database(db_session=db_session)
    compliance_data = ComplianceData()
