#! /usr/bin/env python3
import os
import csv
# import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(os.path.dirname(__file__)).parent))
from aws_allowlister.database.build import build_database
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.compliance_data import ComplianceData

compliance_data = ComplianceData()
db_session = connect_db()


def update_database(download: bool):
    build_database(download)
    compliance_data.update_compliance_database(db_session=db_session)


def update_csv_summary():
    rows = compliance_data.get_rows(db_session=db_session)
    csv_file_path = os.path.join(os.path.dirname(__file__), os.path.pardir, "aws_allowlister", "data",
                                 "compliance_statuses.csv")
    excel_file_path = os.path.join(os.path.dirname(__file__), os.path.pardir, "aws_allowlister", "data",
                                   "compliance_statuses.xlsx")
    # Remove previous CSV file
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    # Remove previous Excel file
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)

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
    print(f"CSV updated! Wrote {len(rows)} rows. Path: {csv_file_path}")

    # df_new = pd.read_csv(csv_file_path)
    # writer = pd.ExcelWriter(excel_file_path)
    # df_new.to_excel(writer, index=False)
    # writer.save()
    # print(f"Excel file updated! Wrote {len(rows)} rows. Path: {excel_file_path}")


if __name__ == '__main__':
    download_docs = True
    update_database(download=download_docs)
    update_csv_summary()
