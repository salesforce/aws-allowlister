import json
import unittest
from aws_allowlister.database.compliance_data import ComplianceData
from aws_allowlister.database.database import connect_db


class ComplianceDataTestCase(unittest.TestCase):
    def test_get_standard_names(self):
        compliance_data = ComplianceData()
        db_session = connect_db()
        result = compliance_data.standard_names(db_session=db_session)
        print(result)
        expected_result = ['SOC', 'PCI', 'ISO', 'FedRAMP', 'HIPAA', 'HITRUST', 'IRAP', 'OSPAR', 'FINMA']
        self.assertListEqual(result, expected_result)

    def test_get_compliance_status(self):
        compliance_data = ComplianceData()
        db_session = connect_db()
        print("getting the status")
        status = compliance_data.get_compliance_status(
            db_session=db_session,
            service_prefix="account",
            compliance_standard="SOC"
        )
        print(status)
        self.assertEqual(status, "true")

    def test_get_compliant_services(self):
        compliance_data = ComplianceData()
        db_session = connect_db()
        standard = "SOC"
        results = compliance_data.get_compliant_services(
            db_session=db_session, compliance_standard=standard
        )
        print(json.dumps(results, indent=4))
        expected_results = [
            "account",
            "acm",
            "amplify",
            "amplifybackend",
            "apigateway",
            "application-autoscaling",
            "appstream",
            "appsync",
            "athena",
            "autoscaling",
            "aws-portal",
            "backup",
            "batch",
            "chime",
            "clouddirectory",
            "cloudformation",
            "cloudfront",
            "cloudhsm",
            "cloudtrail",
            "cloudwatch",
            "codebuild",
            "codecommit",
            "codedeploy",
            "codepipeline",
            "cognito-identity",
            "cognito-idp",
            "comprehend",
            "comprehendmedical",
            "config",
            "connect",
            "dataexchange",
            "datasync",
            "directconnect",
            "dms",
            "ds",
            "dynamodb",
            "ebs",
            "ec2",
            "ecr",
            "ecs",
            "eks",
            "elasticache",
            "elasticbeanstalk",
            "elasticfilesystem",
            "elasticloadbalancing",
            "elasticmapreduce",
            "es",
            "events",
            "execute-api",
            "firehose",
            "fms",
            "forecast",
            "freertos",
            "fsx",
            "glacier",
            "globalaccelerator",
            "glue",
            "greengrass",
            "guardduty",
            "health",
            "iam",
            "inspector",
            "iot",
            "iot-device-tester",
            "iotdeviceadvisor",
            "iotevents",
            "iotwireless",
            "kafka",
            "kinesis",
            "kinesisanalytics",
            "kinesisvideo",
            "kms",
            "lambda",
            "lex",
            "license-manager",
            "logs",
            "macie2",
            "mediaconnect",
            "mediaconvert",
            "medialive",
            "mq",
            "neptune-db",
            "opsworks-cm",
            "organizations",
            "outposts",
            "personalize",
            "polly",
            "qldb",
            "quicksight",
            "rds",
            "rds-data",
            "rds-db",
            "redshift",
            "rekognition",
            "resource-groups",
            "robomaker",
            "route53",
            "route53domains",
            "s3",
            "sagemaker",
            "sdb",
            "secretsmanager",
            "securityhub",
            "serverlessrepo",
            "servicecatalog",
            "ses",
            "shield",
            "sms",
            "sms-voice",
            "snowball",
            "sns",
            "sqs",
            "ssm",
            "sso",
            "sso-directory",
            "states",
            "storagegateway",
            "sts",
            "support",
            "swf",
            "textract",
            "transcribe",
            "transfer",
            "translate",
            "waf",
            "waf-regional",
            "wafv2",
            "workdocs",
            "worklink",
            "workmail",
            "workspaces",
            "xray"
        ]
        print(len(expected_results))
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)
