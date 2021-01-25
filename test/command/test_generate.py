import unittest
import json
from click.testing import CliRunner
from aws_allowlister.command.generate import generate, generate_allowlist_scp


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
        result = self.runner.invoke(generate, ["-fm"])
        self.assertTrue(result.exit_code == 0)

        # Test --exclude
        result = self.runner.invoke(generate, ["--exclude", "iam,s3", "--quiet"])
        self.assertTrue(result.exit_code == 0)
        result_json = json.loads(result.output)
        not_actions = result_json.get("Statement").get("NotAction")
        print(result_json)
        result_json = json.loads(result.output)
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
