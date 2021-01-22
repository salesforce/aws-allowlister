from aws_allowlister.database.build import build_database
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import ComplianceData


def update_data():
    db_session = connect_db()
    build_database()
    compliance_data = ComplianceData()
    compliance_data.update_compliance_database(db_session=db_session)


if __name__ == '__main__':
    update_data()
