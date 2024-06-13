# resources/security.py
import pulumi
import pulumi_aws as aws
from dto import SecurityConfigDTO

class SecurityResource:
    def __init__(self, config: SecurityConfigDTO, vpc_id: pulumi.Output[str]):
        self.config = config
        self.vpc_id = vpc_id
        self.setup_security_groups()
        self.setup_network_acls()

    def setup_security_groups(self):
        for sg in self.config.security_groups:
            group = aws.ec2.SecurityGroup(
                sg.name,
                description=sg.description,
                vpc_id=self.vpc_id,
                ingress=sg.ingress,
                egress=sg.egress
            )
            if 'security_group_ids' not in self.config.outputs:
                self.config.outputs['security_group_ids'] = []
            self.config.outputs['security_group_ids'].append(group.id)

    def setup_network_acls(self):
        for acl in self.config.network_acls:
            nacl = aws.ec2.NetworkAcl(
                acl.name,
                vpc_id=self.vpc_id,
                ingress=acl.ingress,
                egress=acl.egress
            )
            if 'network_acl_ids' not in self.config.outputs:
                self.config.outputs['network_acl_ids'] = []
            self.config.outputs['network_acl_ids'].append(nacl.id)

    def output_dto(self) -> SecurityConfigDTO:
        return self.config
