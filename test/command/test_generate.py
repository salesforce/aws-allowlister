import unittest
import json
from click.testing import CliRunner
from aws_allowlister.command.generate import generate, generate_allowlist_scp, format_allowlist_services, \
    generate_allowlist_service_prefixes


class AllowListerClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_allowlister_with_click(self):
        result = self.runner.invoke(generate, ["-a"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-s"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-p"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-h"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-i"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-fh"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-fm"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-fh"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-d2e"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-d2g"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-d4g"])
        self.assertTrue(result.exit_code == 0)
        result = self.runner.invoke(generate, ["-d5g"])
        self.assertTrue(result.exit_code == 0)        

        # Test --exclude
        result = self.runner.invoke(generate, ["--exclude", "iam,s3", "--quiet"])
        self.assertTrue(result.exit_code == 0)
        result_json = json.loads(result.output)
        not_actions = result_json.get("Statement").get("NotAction")
        self.assertTrue("iam:*" not in not_actions)
        self.assertTrue("s3:*" not in not_actions)

        # Test --include
        result = self.runner.invoke(generate, ["--include", "yolo", "--quiet"])
        self.assertTrue(result.exit_code == 0)
        result_json = json.loads(result.output)
        not_actions = result_json.get("Statement").get("NotAction")
        self.assertTrue("yolo:*" in not_actions)


class GenerateAllowlistScpTestCase(unittest.TestCase):
    def test_generate_with_force_include(self):
        standards = ["PCI"]
        include = ["yolo"]
        exclude = []
        results = generate_allowlist_scp(standards, include=include, exclude=exclude)
        # print(json.dumps(results, indent=4))
        not_actions = results.get("Statement").get("NotAction")
        self.assertTrue("yolo:*" in not_actions)

    def test_generate_with_force_exclude(self):
        standards = ["PCI"]
        include = []
        exclude = ["iam"]
        results = generate_allowlist_scp(standards, include=include, exclude=exclude)
        # print(json.dumps(results, indent=4))
        not_actions = results.get("Statement").get("NotAction")
        # Even though we would never remove IAM from an SCP,
        # this is a good way to demonstrate how services can be forcibly removed from the SCP
        self.assertTrue("iam:*" not in not_actions)


class GenerateMethodsTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_format_allowlist_services(self):
        services = [
            "iam",
            "ssm",
            "s3"
        ]
        # Test out the
        result = format_allowlist_services(services)
        expected_result = ['iam:*', 'ssm:*', 's3:*']
        print(result)
        self.assertListEqual(result, expected_result)

    def test_generate_allowlist_table_format(self):
        result = self.runner.invoke(generate, ["--table"])
        self.assertTrue(result.exit_code == 0)
        # If --table is used, it should include the string "Service Prefix"
        self.assertTrue("Service Prefix" in result.output)
        # It should also have a real service name somewhere in the output - like "Amazon S3"
        self.assertTrue("Amazon S3" in result.output)

    def test_generate_allowlist_in_json_format(self):
        # If --table is used, it should include elements that are in an IAM Policy but not in the markdown formatted table
        result = self.runner.invoke(generate, [])
        self.assertTrue(result.exit_code == 0)
        # If --table is NOT used, then it will look like an IAM policy, so it will have NotAction (an IAM Policy element) in the output.
        self.assertTrue("NotAction" in result.output)
        # It shouldn't have Amazon S3 (expected in markdown table) when output is the default json
        self.assertTrue("Amazon S3" not in result.output)

