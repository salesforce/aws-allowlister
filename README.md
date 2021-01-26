# aws-allowlister

![Continuous Integration Tests](https://github.com/salesforce/aws-allowlister/workflows/continuous-integration/badge.svg)


Automatically compile an AWS Service Control Policy that ONLY allows AWS services that are compliant with your selected frameworks. Supports SOC, PCI, HIPAA, ISO, FedRAMP High, and FedRAMP Moderate.

## Installation

* Python Pip:

```bash
pip3 install aws-allowlister
```

* Homebrew (this will work once we open source it):

```bash
brew tap salesforce/aws-allowlister https://github.com/salesforce/aws-allowlister
brew install aws-allowlister
```

## Usage

* Generate an AllowList Policy using this command:

```bash
aws-allowlister generate
```

By default, it allows policies at the intersection of PCI, HIPAA, SOC, ISO, FedRAMP High, and FedRAMP Moderate.

The resulting policy will look like this:

<details>
<summary>Example AllowList Policy</summary>

```json
{
    "Version": "2012-10-17",
    "Statement": {
        "Sid": "AllowList",
        "Effect": "Deny",
        "NotAction": [
            "account:*",
            "acm:*",
            "amplify:*",
            "amplifybackend:*",
            "apigateway:*",
            "application-autoscaling:*",
            "appstream:*",
            "appsync:*",
            "athena:*",
            "autoscaling:*",
            "aws-portal:*",
            "backup:*",
            "batch:*",
            "clouddirectory:*",
            "cloudformation:*",
            "cloudfront:*",
            "cloudhsm:*",
            "cloudtrail:*",
            "cloudwatch:*",
            "codebuild:*",
            "codecommit:*",
            "codedeploy:*",
            "codepipeline:*",
            "cognito-identity:*",
            "cognito-idp:*",
            "comprehend:*",
            "comprehendmedical:*",
            "config:*",
            "connect:*",
            "dataexchange:*",
            "datasync:*",
            "directconnect:*",
            "dms:*",
            "ds:*",
            "dynamodb:*",
            "ebs:*",
            "ec2:*",
            "ecr:*",
            "ecs:*",
            "eks:*",
            "elasticache:*",
            "elasticbeanstalk:*",
            "elasticfilesystem:*",
            "elasticmapreduce:*",
            "es:*",
            "events:*",
            "execute-api:*",
            "firehose:*",
            "fms:*",
            "forecast:*",
            "freertos:*",
            "fsx:*",
            "glacier:*",
            "globalaccelerator:*",
            "glue:*",
            "greengrass:*",
            "guardduty:*",
            "health:*",
            "iam:*",
            "inspector:*",
            "iot:*",
            "iot-device-tester:*",
            "iotdeviceadvisor:*",
            "iotevents:*",
            "iotwireless:*",
            "kafka:*",
            "kinesis:*",
            "kinesisanalytics:*",
            "kinesisvideo:*",
            "kms:*",
            "lambda:*",
            "lex:*",
            "logs:*",
            "macie2:*",
            "mediaconnect:*",
            "mediaconvert:*",
            "medialive:*",
            "mq:*",
            "neptune-db:*",
            "opsworks-cm:*",
            "organizations:*",
            "outposts:*",
            "personalize:*",
            "polly:*",
            "qldb:*",
            "quicksight:*",
            "rds:*",
            "rds-data:*",
            "rds-db:*",
            "redshift:*",
            "rekognition:*",
            "robomaker:*",
            "route53:*",
            "route53domains:*",
            "s3:*",
            "sagemaker:*",
            "secretsmanager:*",
            "securityhub:*",
            "serverlessrepo:*",
            "servicecatalog:*",
            "shield:*",
            "sms:*",
            "sms-voice:*",
            "snowball:*",
            "sns:*",
            "sqs:*",
            "ssm:*",
            "sso:*",
            "sso-directory:*",
            "states:*",
            "storagegateway:*",
            "sts:*",
            "support:*",
            "swf:*",
            "textract:*",
            "transcribe:*",
            "transfer:*",
            "translate:*",
            "waf:*",
            "waf-regional:*",
            "wafv2:*",
            "workdocs:*",
            "worklink:*",
            "workspaces:*",
            "xray:*"
        ],
        "Resource": "*"
    }
}
```

</details>

## Arguments

`aws-allowlister` supports different arguments to generate fine-grained compliance focused Service Control Policy (SCP) AllowLists. You can specify individual flags for the compliance frameworks you care about.

```
Usage: aws-allowlister generate [OPTIONS]

Options:
  -a, --all                SOC, PCI, ISO, HIPAA, FedRAMP_High, and
                           FedRAMP_Moderate.

  -s, --soc                Include SOC-compliant services
  -p, --pci                Include PCI-compliant services
  -h, --hipaa              Include HIPAA-compliant services
  -i, --iso                Include ISO-compliant services
  -fh, --fedramp-high      Include FedRAMP High
  -fm, --fedramp-moderate  Include FedRAMP Moderate
  --include TEXT           Include specific AWS IAM services, specified in a
                           comma separated string.

  --exclude TEXT           Exclude specific AWS IAM services, specified in a
                           comma separated string.

  -q, --quiet
  --help                   Show this message and exit.
```


* For example, to generate a PCI only Service Control Policy and save it to JSON:

```bash
aws-allowlister generate --pci --quiet > pci.json
```

* You can also chain command flags together. For example, to generate a Policy for all the major compliance frameworks but FedRAMP:

```bash
aws-allowlister generate -sphi --quiet
```

* Let's say your organization is not subject to FedRAMP or HIPAA, but you want to create a Policy for PCI, SOC, and ISO:

```bash
aws-allowlister generate -spi --quiet
```

# Contributing

## Setup

* Set up the virtual environment

```bash
# Set up the virtual environment
python3 -m venv ./venv && source venv/bin/activate
pip3 install -r requirements.txt
```

* Build the package

```bash
# To build only
make build

# To build and install
make install

# To run tests
make test

# To clean local dev environment
make clean
```

# Authors and Contributors

* [Kinnaird McQuade (@kmcquade3)](https://twitter.com/kmcquade3), Salesforce - Author
* [Jason Dyke (@jasonadyke)](https://twitter.com/jasonadyke), ScaleSec - Contributor

# Disclaimer
The policies generated by `aws-allowlister` do not guarantee that your AWS accounts will be compliant or that you will become accredited with the supported compliance frameworks. These policies are intended to be a useful tool to assist with restricting which service can or cannot be leveraged.
