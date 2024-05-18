# YAML Configuration for Security Settings
security:
  security_groups:
    - name: web-server-sg
      description: "Security group for web servers"
      vpc_id: "${vpc_id}"  # This will be populated dynamically
      ingress:
        - protocol: "tcp"
          from_port: 80
          to_port: 80
          cidr_blocks: ["0.0.0.0/0"]
      egress:
        - protocol: "-1"
          from_port: 0
          to_port: 0
          cidr_blocks: ["0.0.0.0/0"]
  network_acls:
    - name: web-acl
      vpc_id: "${vpc_id}"  # This will be populated dynamically
      ingress:
        - rule_number: 100
          protocol: "tcp"
          rule_action: "allow"
          cidr_block: "0.0.0.0/0"
          from_port: 80
          to_port: 80
      egress:
        - rule_number: 100
          protocol: "-1"
          rule_action: "allow"
          cidr_block: "0.0.0.0/0"
          from_port: 0
          to_port: 0
  outputs:
    security_group_ids: []
    network_acl_ids: []

# resources/security.py
import pulumi_aws as aws
from dto import SecurityConfigDTO

class SecurityResource:
    def __init__(self, config: SecurityConfigDTO):
        self.config = config
        self.setup_security_groups()
        self.setup_network_acls()

    def setup_security_groups(self):
        for sg in self.config.security_groups:
            group = aws.ec2.SecurityGroup(
                sg.name,
                description=sg.description,
                vpc_id=sg.vpc_id,
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
                vpc_id=acl.vpc_id,
                ingress=acl.ingress,
                egress=acl.egress
            )
            if 'network_acl_ids' not in self.config.outputs:
                self.config.outputs['network_acl_ids'] = []
            self.config.outputs['network_acl_ids'].append(nacl.id)

    def output_dto(self) -> SecurityConfigDTO:
        return self.config


