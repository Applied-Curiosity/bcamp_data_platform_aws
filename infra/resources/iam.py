# resources/iam.py
import pulumi_aws as aws
from dto import IAMConfigDTO

# ty working on python pathing issue

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
