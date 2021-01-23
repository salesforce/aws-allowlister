import os
from policy_sentry.querying.all import get_all_service_prefixes
from aws_allowlister.shared.utils import read_yaml_file

ALL_SERVICE_PREFIXES = get_all_service_prefixes()


class Overrides:
    def __init__(self):
        overrides_file = os.path.join(
            os.path.dirname(__file__), os.path.pardir, "data", "overrides.yml"
        )
        self.overrides = read_yaml_file(overrides_file)
        self.service_names_to_iam_names = self.overrides.get(
            "service_names_to_iam_names"
        )
        self.sdk_names_to_iam_names = self.overrides.get("sdk_names_to_iam_names")
        self.global_inserts = self.overrides.get("global_inserts")
        self.direct_inserts = self.overrides.get("direct_inserts")
        self.direct_removals = self.overrides.get("direct_removals")

    def get_iam_names_matching_service_name(self, service_name):
        iam_names = []
        if self.service_names_to_iam_names.get(service_name):
            iam_names.extend(self.service_names_to_iam_names.get(service_name))
        return iam_names

    def get_iam_names_matching_sdk_name(self, sdk_name):
        iam_names = []
        if self.sdk_names_to_iam_names.get(sdk_name):
            iam_names.extend(self.sdk_names_to_iam_names.get(sdk_name))
        return iam_names
