import os
import csv
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db

compliance_data = ComplianceData()
db_session = connect_db()


def update_csv():
    print()
    rows = compliance_data.get_rows(db_session=db_session)
    csv_file_path = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        "aws_allowlister",
        "data",
        "compliance_statuses.csv"
    )
    # Remove previous CSV file
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    standards = compliance_data.standard_names(db_session=db_session)
    field_names = [
        "service_prefix",
        "name",
    ]
    field_names.extend(standards)
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"CSV updated! Wrote {len(rows)} rows.")


if __name__ == '__main__':
    update_csv()
