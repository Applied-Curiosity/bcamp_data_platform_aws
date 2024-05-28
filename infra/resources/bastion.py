# resources/bastion.py
import pulumi_aws as aws
from dto import BastionConfigDTO

class BastionResource:
    def __init__(self, config: BastionConfigDTO):
        self.config = config
        self.instance = self.create_instance()

    def create_instance(self):
        instance = aws.ec2.Instance(
            self.config.instance['name'],
            ami=self.config.instance['ami'],
            instance_type=self.config.instance['instance_type'],
            key_name=self.config.instance['key_name'],
            vpc_security_group_ids=self.config.instance['vpc_security_group_ids'],
            subnet_id=self.config.instance['subnet_id'],
            associate_public_ip_address=self.config.instance['associate_public_ip_address'],
            tags={"Name": self.config.instance['name']}
        )
        # Store outputs
        self.config.outputs['instance_id'] = instance.id
        self.config.outputs['public_ip'] = instance.public_ip

        return instance

    def output_dto(self) -> BastionConfigDTO:
        return self.config
