# resources/iam.py

from pathlib import Path
import sys
import importlib.util

# ty working on pathing issue
site_package_dir = Path('/workspaces/bcamp_data_platform_aws/infra/venv/lib64/python3.10/site-packages')
sys.path.append(str(site_package_dir)) # append path with site dependencies to the main path


import pulumi_aws as aws # still gives issue with grpc
from dto import IAMConfigDTO

class IAMResource:
    def __init__(self, config: IAMConfigDTO):
        self.config = config
        self.setup_roles()

    def setup_roles(self):
        for role in self.config.roles:
            iam_role = aws.iam.Role(
                role.name,
                assume_role_policy=role.assume_role_policy
            )
            for policy_arn in role.policies:
                aws.iam.RolePolicyAttachment(
                    f"{role.name}-{policy_arn.split('/')[-1]}",
                    role=iam_role.name,
                    policy_arn=policy_arn
                )
            # Capture the ARN of the created role in the DTO
            if 'role_arns' not in self.config.outputs:
                self.config.outputs['role_arns'] = []
            self.config.outputs['role_arns'].append(iam_role.arn)

    def output_dto(self) -> IAMConfigDTO:
        return self.config
