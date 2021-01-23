import unittest
import json
from aws_allowlister.database.database import connect_db
from aws_allowlister.database.raw_scraping_data import RawScrapingData

db_session = connect_db()
raw_scraping_data = RawScrapingData()


class RawScrapingDataTestCase(unittest.TestCase):
    def test_standards(self):
        """database.scrapers.raw_scraping_data.standards"""
        results = raw_scraping_data.standards(db_session=db_session)
        print(results)
        print(len(results))
        # This will grow over time, so let's just make sure it meets minimum size
        self.assertTrue(len(results) >= 7)
        expected_results = ['SOC', 'PCI', 'IRAP', 'OSPAR', 'FINMA', 'ISO', 'HIPAA']


    def test_get_rows(self):
        """database.scrapers.raw_scraping_data.get_rows"""
        results = raw_scraping_data.get_rows(db_session=db_session, sdk_name="ecs")
        print(len(results))
        # print(results)
        results = raw_scraping_data.get_rows(db_session=db_session)
        # This will change over time, so let's just check that the size of this is massive
        print(len(results))
        self.assertTrue(len(results) > 850)  # 857

    def test_get_sdk_names_matching_compliance_standard(self):
        """database.scrapers.raw_scraping_data.get_sdk_names_matching_compliance_standard"""
        results = raw_scraping_data.get_sdk_names_matching_compliance_standard(db_session=db_session, standard_name="SOC")
        # print(results)
        print(len(results))  # 120

    def test_get_service_names_matching_compliance_standard(self):
        """database.scrapers.raw_scraping_data.get_service_names_matching_compliance_standard"""
        results = raw_scraping_data.get_service_names_matching_compliance_standard(db_session=db_session, standard_name="SOC")
        # print(results)
        print(len(results))  # 119
        expected_results = {'Amazon API Gateway': 'apigateway', 'Amazon AppStream 2.0': 'appstream', 'Amazon Athena': 'athena', 'Amazon Chime': 'chime', 'Amazon Cloud Directory': 'clouddirectory', 'Amazon CloudFront': 'cloudfront', 'Amazon CloudWatch': 'cloudwatch', 'Amazon CloudWatch Events [includes Amazon EventBridge]': 'events', 'Amazon CloudWatch Logs': 'logs', 'Amazon CloudWatch SDK Metrics for Enterprise Support': 'sdkmetrics', 'Amazon Cognito': 'cognito-sync', 'Amazon Comprehend': 'comprehend', 'Amazon Comprehend Medical': 'comprehendmedical', 'Amazon Connect': 'connect', 'Amazon DynamoDB': 'dynamodb', 'Amazon EC2 Auto Scaling': 'autoscaling', 'Amazon Elastic Block Store (EBS)': 'ec2', 'Amazon Elastic Compute Cloud (EC2)': 'ec2', 'Amazon Elastic Container Registry (ECR)': 'ecr', 'Amazon Elastic Container Service': 'ecs', 'Amazon Elastic File System (EFS)': 'elasticfilesystem', 'Amazon Elastic Kubernetes Service (EKS)': 'eks', 'Amazon Elastic MapReduce (EMR)': 'elasticmapreduce', 'Amazon ElastiCache for Redis': 'elasticache', 'Amazon Elasticsearch Service': 'es', 'Amazon Forecast': 'amazonforecast', 'Amazon FreeRTOS': 'freertos', 'Amazon FSx': 'fsx', 'Amazon GuardDuty': 'guardduty', 'Amazon Inspector': 'inspector', 'Amazon Kinesis Data Analytics': 'kinesisanalytics', 'Amazon Kinesis Data Firehose': 'firehose', 'Amazon Kinesis Data Streams': 'kinesis', 'Amazon Kinesis Video Streams': 'kinesisvideo', 'Amazon Lex': 'models.lex', 'Amazon Macie': 'macie', 'Amazon Managed Streaming for Apache Kafka': 'kafka', 'Amazon MQ': 'mq', 'Amazon Neptune': 'neptune-db', 'Amazon Personalize': 'personalize', 'Amazon Pinpoint': 'mobiletargeting', 'Amazon Polly': 'polly', 'Amazon Quantum Ledger Database (QLDB)': 'qldb', 'Amazon QuickSight': 'quicksight', 'Amazon Redshift': 'redshift', 'Amazon Rekognition': 'rekognition', 'Amazon Relational Database Service (RDS)': 'rds', 'Amazon Route 53': 'route53', 'Amazon S3 Glacier': 'glacier', 'Amazon SageMaker': 'sagemaker', 'Amazon SimpleDB': 'sdb', 'Amazon Simple Email Service (SES)': 'ses', 'Amazon Simple Notification Service (SNS)': 'sns', 'Amazon Simple Queue Service (SQS)': 'sqs', 'Amazon Simple Storage Service (S3)': 's3', 'Amazon Simple Workflow Service (SWF)': 'swf', 'Amazon Textract': 'textract', 'Amazon Transcribe': 'transcribe', 'Amazon Translate': 'translate', 'Amazon Virtual Private Cloud (VPC)': 'ec2', 'Amazon WorkDocs': 'workdocs', 'Amazon WorkLink': 'worklink', 'Amazon WorkMail': 'workmail', 'Amazon WorkSpaces': 'workspaces', 'AWS Amplify': 'amplify', 'AWS AppSync': 'appsync', 'AWS Backup': 'backup', 'AWS Batch': 'batch', 'AWS Certificate Manager (ACM)': 'acm', 'AWS CloudFormation': 'cloudformation', 'AWS CloudHSM': 'cloudhsm', 'AWS CloudTrail': 'cloudtrail', 'AWS CodeBuild': 'codebuild', 'AWS CodeCommit': 'codecommit', 'AWS CodeDeploy': 'codedeploy', 'AWS CodePipeline': 'codepipeline', 'AWS Config': 'config', 'AWS Control Tower': 'controltower', 'AWS Data Exchange': 'dataexchange', 'AWS Database Migration Service (DMS)': 'dms', 'AWS DataSync': 'datasync', 'AWS Direct Connect': 'directconnect', 'AWS Directory Service': 'ds', 'AWS Elastic Beanstalk': 'elasticbeanstalk', 'AWS Elemental MediaConnect': 'mediaconnect', 'AWS Elemental MediaConvert': 'mediaconvert', 'AWS Elemental MediaLive': 'medialive', 'AWS Firewall Manager': 'fms', 'AWS Global Accelerator': 'globalaccelerator', 'AWS Glue': 'glue', 'AWS Identity and Access Management (IAM)': 'iam', 'AWS IoT Core': 'iot', 'AWS IoT Device Management': 'iot', 'AWS IoT Events': 'iotevents', 'AWS IoT Greengrass': 'greengrass', 'AWS Key Management Service (KMS)': 'kms', 'AWS Lambda': 'lambda', 'AWS License Manager': 'license-manager', 'AWS OpsWorks Stacks': 'opsworks', 'AWS OpsWorks Stacksfor Chef Automate': 'opsworks-cm', 'AWS Organizations': 'organizations', 'AWS Outposts': 'outposts', 'AWS Personal Health Dashboard': 'health', 'AWS Resource Groups': 'resource-groups', 'AWS RoboMaker': 'robomaker', 'AWS Secrets Manager': 'secretsmanager', 'AWS Security Hub': 'securityhub', 'AWS Server Migration Service (SMS)': 'sms', 'AWS Serverless Application Repository': 'serverlessrepo', 'AWS Service Catalog': 'servicecatalog', 'AWS Shield': 'DDoSProtection', 'AWS Snowball': 'snowball', 'AWS Step Functions': 'states', 'AWS Storage Gateway': 'storagegateway', 'AWS Systems Manager': 'ssm', 'AWS Transfer Family': 'transfer', 'AWS Web Application Firewall (WAF)': 'waf', 'AWS X-Ray': 'xray', 'Elastic Load Balancing (ELB)': 'elasticloadbalancing'}

