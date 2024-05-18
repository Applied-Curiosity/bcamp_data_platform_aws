# VPC Resource Class
import pulumi_aws as aws
from dto import VPCConfigDTO

class VPCResource:
    def __init__(self, config: VPCConfigDTO):
        self.config = config
        self.setup_vpc()

    def setup_vpc(self):
        vpc = aws.ec2.Vpc(self.config.name, cidr_block=self.config.cidr_block)

        if self.config.internet_gateway:
            ig = aws.ec2.InternetGateway(f"{self.config.name}-ig", vpc_id=vpc.id)

        subnet_ids = []
        for subnet in self.config.subnets:
            sn = aws.ec2.Subnet(
                f"{subnet.name}-{self.config.name}",
                vpc_id=vpc.id,
                cidr_block=subnet.cidr_block,
                availability_zone=subnet.availability_zone,
                map_public_ip_on_launch=subnet.map_public_ip_on_launch
            )
            subnet_ids.append(sn.id)

        # Store outputs
        self.config.outputs['vpc_id'] = vpc.id
        self.config.outputs['subnet_ids'] = subnet_ids

    def output_dto(self) -> VPCConfigDTO:
        return self.config

