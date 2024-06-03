import pulumi_aws as aws
from dto import IAMConfigDTO
import pulumi

class IAMResource:
    def __init__(self, config: IAMConfigDTO):
        self.config = config
        self.role_arns = []
        self.setup_roles()

    def setup_roles(self):
        for role in self.config.roles:
            print(f"Creating IAM role: {role.name}")

            # Use the assume_role_policy directly from the role configuration
            assume_role_policy = role.assume_role_policy

            # Create the IAM Role
            iam_role = aws.iam.Role(
                role.name,
                assume_role_policy=assume_role_policy,
                tags=role.tags.to_dict(),
            )

            # Attach the policies to the IAM Role
            for policy_arn in role.policies:
                if isinstance(policy_arn, dict):
                    policy_arn = policy_arn.get('arn', '')
                if not isinstance(policy_arn, str) or not policy_arn:
                    raise ValueError(f"Invalid policy ARN: {policy_arn}")
                print(f"Attaching policy {policy_arn} to role {role.name}")
                aws.iam.RolePolicyAttachment(
                    f"{role.name}-{policy_arn.split('/')[-1]}",
                    role=iam_role.name,
                    policy_arn=policy_arn
                )

            # Capture the ARN of the created role in the DTO using apply
            iam_role.arn.apply(lambda arn: self.capture_role_arn(role.name, arn))

    def capture_role_arn(self, role_name: str, arn: str):
        if 'role_arns' not in self.config.outputs:
            self.config.outputs['role_arns'] = []
        self.config.outputs['role_arns'].append({role_name: arn})
        print(f"Created IAM role ARN: {arn}")

    def output_dto(self) -> IAMConfigDTO:
        return self.config
