import logging
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.shared.iam_data import get_service_prefix_data
from aws_allowlister.database.database import TransformedScrapingDataTable, RawScrapingDataTable
from aws_allowlister.database.raw_scraping_data import RawScrapingData
from aws_allowlister.scrapers.overrides import Overrides
from aws_allowlister.shared.utils import get_service_name_matching_iam_service_prefix, \
    clean_service_name_after_brackets_and_parentheses

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
ALL_SERVICE_PREFIXES = get_all_service_prefixes()


class TransformedScrapingData:
    def __init__(self):
        self.note = None

    def standards(self, db_session):
        """"
        Let's get the list of standards from the RawScrapingDataTable in case the Transformed data table is not populated yet.
        """
        query = db_session.query(
            RawScrapingDataTable.compliance_standard_name.distinct().label(
                "compliance_standard_name"
            )
        )
        standards = [row.compliance_standard_name for row in query.all()]
        # Note to self: this could also be accomplished with:
        # results = transformed_scraping_database.get_rows(db_session=db_session, service_prefix="s3")
        # list(set(map(lambda x: x.get("compliance_standard_name"), results)))
        return standards

    def get_rows(self, db_session, service_prefix=None, service_name=None, standard=None):
        """Get rows as a list of dictionaries"""
        if service_prefix:
            rows = db_session.query(TransformedScrapingDataTable).filter(
                TransformedScrapingDataTable.sdk_name == service_prefix
            )
        elif service_name:
            rows = db_session.query(TransformedScrapingDataTable).filter(
                TransformedScrapingDataTable.service_name == service_name
            )
        elif standard:
            rows = db_session.query(TransformedScrapingDataTable).filter(
                TransformedScrapingDataTable.compliance_standard_name == standard
            )
        else:
            rows = db_session.query(TransformedScrapingDataTable)
        size = len(rows.all())
        results = []
        for row in rows:
            res = row.__dict__
            res.pop("_sa_instance_state", None)
            res.pop("id", None)
            results.append(row.__dict__)
        return results

    def get_sdk_names_matching_compliance_standard(self, db_session, standard_name):
        """
        Get a list of all SDK names matching this compliance standard from the TransformedScrapingDataTable
        """
        rows = db_session.query(TransformedScrapingDataTable).filter(
            TransformedScrapingDataTable.compliance_standard_name == standard_name
        )
        sdk_names = {}
        for row in rows:
            sdk_names[row.sdk_name] = row.service_name
        return sdk_names

    def get_service_names_matching_compliance_standard(self, db_session, standard_name):
        """
        Get a list of all SDK names matching this compliance standard from the TransformedScrapingDataTable
        """
        rows = db_session.query(TransformedScrapingDataTable).filter(
            TransformedScrapingDataTable.compliance_standard_name == standard_name
        )
        service_names = {}
        for row in rows:
            service_names[row.service_name] = row.sdk_name
        return service_names

    def set_sdk_name_given_service_name(self, db_session, service_name, sdk_name):
        """Set the SDK name given the name of the AWS Service"""
        service_name = clean_service_name_after_brackets_and_parentheses(service_name)
        rows = db_session.query(TransformedScrapingDataTable).filter(
            TransformedScrapingDataTable.service_name == service_name
        )
        rows.update({"sdk_name": sdk_name})
        db_session.commit()
        db_session.close()

    def set_service_name_given_sdk_name(self, db_session, service_name, sdk_name):
        """Set the name of the service given the name of the SDK"""
        service_name = clean_service_name_after_brackets_and_parentheses(service_name)
        rows = db_session.query(TransformedScrapingDataTable).filter(
            TransformedScrapingDataTable.sdk_name == sdk_name
        )
        rows.update({"service_name": service_name})
        db_session.commit()
        db_session.close()

    def add_entry_to_database(self, db_session, compliance_standard_name, service_name, sdk_name):
        """Add an entry to the database"""
        service_name = clean_service_name_after_brackets_and_parentheses(service_name)
        db_session.add(
            TransformedScrapingDataTable(
                compliance_standard_name=compliance_standard_name,
                sdk_name=sdk_name,
                service_name=service_name,
            )
        )
        db_session.commit()

    def populate_table(self, db_session, overrides):
        """Populate the Table using the initial Scraping Data, then apply the overrides"""
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")

        logger.info("Matching names in all compliance standards with their IAM names")

        old_rows = db_session.query(RawScrapingDataTable)
        logger.info("Populating the TransformedScrapingDataTable with the Raw Scraping Data initially")
        for old_row in old_rows:
            exists = db_session.query(TransformedScrapingDataTable).filter_by(
                    compliance_standard_name=old_row.compliance_standard_name,
                    service_name=old_row.service_name,
                    sdk_name=old_row.sdk_name,
                ).first()
            if not exists:
                self.add_entry_to_database(
                    db_session=db_session,
                    compliance_standard_name=old_row.compliance_standard_name,
                    service_name=clean_service_name_after_brackets_and_parentheses(old_row.service_name),
                    sdk_name=old_row.sdk_name,
                )
        logger.info("Applying overrides to the TransformedScrapingDataTable")
        self.transform_database_by_matching_compliance_standard_names_with_iam_names(db_session=db_session)
        self.apply_name_fixes(db_session=db_session, overrides=overrides)

    def transform_database_by_matching_compliance_standard_names_with_iam_names(self, db_session):
        standards = self.standards(db_session=db_session)
        raw_scraping_data = RawScrapingData()
        for standard in standards:
            # The service name in IAM-land
            iam_service_names = {}
            for service_prefix in ALL_SERVICE_PREFIXES:
                iam_service_names[service_prefix] = get_service_prefix_data(service_prefix)[
                    "service_name"
                ]
            # The service name in compliance land
            # Let's get it from the scraping data table because we haven't fully populated the transformed table yet
            standard_service_names = raw_scraping_data.get_service_names_matching_compliance_standard(
                db_session, standard
            )
            # We are going to compare the names of the services that the HIPAA docs say to the ones in the database
            # To do this properly, we need to clean up service names that look like this:
            #   'Amazon Aurora [MySQL, PostgreSQL]'
            #   'Amazon Elastic Container Registry (ECR)'
            # And turn them into this:
            #   'Amazon Aurora'
            #   'Amazon Elastic Container Registry
            # Let's clean it up. We'll store it in this dict
            compliance_service_names = {}
            # Clean the compliance names *before* comparing them to the IAM names
            for compliance_name in standard_service_names.keys():
                service_prefix = standard_service_names.get(compliance_name)
                service_name = clean_service_name_after_brackets_and_parentheses(compliance_name)
                compliance_service_names[service_prefix] = service_name

            compliance_names = []
            for item in iam_service_names:
                compliance_names.append(iam_service_names.get(item))

            for iam_service_prefix in list(iam_service_names.keys()):
                iam_name = iam_service_names[iam_service_prefix]
                for name in compliance_names:
                    if iam_name.lower() == name.lower():
                        self.set_sdk_name_given_service_name(
                            db_session=db_session,
                            service_name=iam_name,
                            sdk_name=iam_service_prefix,
                        )
                        logger.debug(f"match_compliance_standard_name_with_iam_prefix_name: iam_name={iam_name}, "
                              f"sdk_name={iam_service_prefix}")

    def apply_name_fixes(self, db_session, overrides):
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")
        self.override_sdk_names_to_iam_names(db_session=db_session, overrides=overrides)
        self.override_service_names_to_iam_names(
            db_session=db_session, overrides=overrides
        )
        self.override_global_inserts(db_session=db_session, overrides=overrides)
        db_session.commit()

    def override_service_names_to_iam_names(self, db_session, overrides):
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")
        print("\nOVERRIDES: SECTION 1: override_service_names_to_iam_names")
        print(
            "\nApplying overrides to the database: Section 1, 'Service name means IAM name'"
        )
        staging_area = {}
        content_to_remove = []
        for service_name in overrides.service_names_to_iam_names:
            rows = db_session.query(TransformedScrapingDataTable).filter(
                TransformedScrapingDataTable.service_name == service_name
            )
            print(f"\n{service_name}: {rows.count()}")
            matching_standards = []
            print(f"\tCurrent content:")
            for row in rows:
                content = {
                    "compliance_standard_name": row.compliance_standard_name,
                    "service_name": row.service_name,
                    "sdk_name": row.sdk_name,
                }
                print(f"\t{content}")
                content_to_remove.append(content)
                matching_standards.append(row.compliance_standard_name)
            print(f"\t{service_name}'s matching standards: {matching_standards}")
            for iam_name in overrides.service_names_to_iam_names.get(service_name):
                if not staging_area.get(service_name):
                    staging_area[service_name] = []
                for matching_standard in matching_standards:
                    content = {
                        "compliance_standard_name": matching_standard,
                        "service_name": service_name,
                        "sdk_name": iam_name,
                    }
                    print(f"\tAdding to staging area: {content}")
                    staging_area[service_name].append(content)
        # Let's remove the old content since we are going to add the new stuff
        print("\nRemoving the old content:")
        for old_content in content_to_remove:
            print(f"\t{old_content}")
            row = db_session.query(TransformedScrapingDataTable).filter_by(
                compliance_standard_name=old_content.get("compliance_standard_name"),
                service_name=old_content.get("service_name"),
                sdk_name=old_content.get("sdk_name"),
            )
            row.delete()
            db_session.commit()

        # Using the staging area to add to the database
        print("\nAdding new content to the database")
        for service_name in staging_area:
            print(f"{service_name}: {len(staging_area.get(service_name))}")
            print("\tNew content:")
            for entry in staging_area.get(service_name):
                print(f"\t{entry}")
                exists = (
                    db_session.query(TransformedScrapingDataTable)
                    .filter_by(
                        compliance_standard_name=entry.get("compliance_standard_name"),
                        service_name=entry.get("service_name"),
                        sdk_name=entry.get("sdk_name"),
                    )
                    .first()
                )
                if not exists:
                    self.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name=entry.get("compliance_standard_name"),
                        service_name=entry.get("service_name"),
                        sdk_name=entry.get("sdk_name"),
                    )

    def override_sdk_names_to_iam_names(self, db_session, overrides):
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")
        print("\nOVERRIDES: SECTION 2: override_sdk_names_to_iam_names")
        staging_area = {}
        content_to_remove = []
        for sdk_name in overrides.sdk_names_to_iam_names:
            rows = db_session.query(TransformedScrapingDataTable).filter(
                TransformedScrapingDataTable.sdk_name == sdk_name
            )
            print(f"\n{sdk_name}: {rows.count()}")
            matching_standards = []
            print(f"\tCurrent content:")
            for row in rows:
                content = {
                    "compliance_standard_name": row.compliance_standard_name,
                    "service_name": row.service_name,
                    "sdk_name": row.sdk_name,
                }
                print(f"\t{content}")
                content_to_remove.append(content)
                matching_standards.append(row.compliance_standard_name)
            print(f"\t{sdk_name}'s matching standards: {matching_standards}")
            for iam_name in overrides.sdk_names_to_iam_names.get(sdk_name):
                staging_area[iam_name] = []
                for matching_standard in matching_standards:
                    if not staging_area.get(iam_name):
                        staging_area[iam_name] = []
                    content = {
                        "compliance_standard_name": matching_standard,
                        "service_name": get_service_name_matching_iam_service_prefix(
                            iam_name
                        ),
                        "sdk_name": iam_name,
                    }
                    # print(f"\t{iam_name}")
                    print(f"\tAdding to staging area: {content}")
                    staging_area[iam_name].append(content)
        # Let's remove the old content since we are going to add the new stuff
        print("\nRemoving the old content:")
        for old_content in content_to_remove:
            print(f"\t{old_content}")
            row = db_session.query(TransformedScrapingDataTable).filter_by(
                compliance_standard_name=old_content.get("compliance_standard_name"),
                service_name=old_content.get("service_name"),
                sdk_name=old_content.get("sdk_name"),
            )
            row.delete()
            db_session.commit()

        # Using the staging area to add to the database
        print("\nAdding new content to the database")
        for iam_name in staging_area:
            print(f"{iam_name}: {len(staging_area.get(iam_name))}")
            print("\tNew content:")
            for entry in staging_area.get(iam_name):
                # for entry in staging_area.get(iam_name).get(standard):
                print(f"\t{str(entry)}")
                exists = (
                    db_session.query(TransformedScrapingDataTable)
                    .filter_by(
                        compliance_standard_name=entry.get("compliance_standard_name"),
                        service_name=entry.get("service_name"),
                        sdk_name=entry.get("sdk_name"),
                    )
                    .first()
                )
                if not exists:
                    self.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name=entry.get("compliance_standard_name"),
                        service_name=entry.get("service_name"),
                        sdk_name=entry.get("sdk_name"),
                    )

    def override_global_inserts(self, db_session, overrides):
        if not isinstance(overrides, Overrides):
            raise Exception("Overrides should be an object class of type Overrides")
        standards = self.standards(db_session=db_session)
        print("\nOVERRIDES: SECTION 3: override_global_inserts")
        print("New content:")
        for standard in standards:
            for service_prefix in overrides.global_inserts:
                exists = db_session.query(TransformedScrapingDataTable).filter_by(
                    compliance_standard_name=standard, sdk_name=service_prefix).first()
                if not exists:
                    service_name = get_service_name_matching_iam_service_prefix(
                        service_prefix
                    )
                    if not service_name:
                        service_name = service_prefix.capitalize()
                    content = dict(
                        compliance_standard_name=standard,
                        service_name=service_name,
                        sdk_name=service_prefix,
                    )
                    print(f"\t{content}")
                    self.add_entry_to_database(
                        db_session=db_session,
                        compliance_standard_name=standard,
                        service_name=service_name,
                        sdk_name=service_prefix,
                    )

