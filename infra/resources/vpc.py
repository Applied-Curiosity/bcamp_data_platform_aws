# resources/vpc.py
import pulumi
from pulumi_aws import ec2
from dto import VPCConfigDTO

class VPC:
    def __init__(self, config):
        self.config = config

        # Create VPC
        vpc = ec2.Vpc(self.config.name, cidr_block=self.config.cidr_block)

        # Create Internet Gateway and attach it to the VPC
        ig = ec2.InternetGateway(f"{self.config.name}-ig", vpc_id=vpc.id)
        ec2.VpcInternetGatewayAttachment(f"{self.config.name}-ig-attachment", vpc_id=vpc.id, internet_gateway_id=ig.id)

        # Create a public and private subnet
        subnet_ids = []
        for subnet in self.config.subnets:
            sn = ec2.Subnet(
                f"{subnet['name']}-{self.config.name}",
                vpc_id=vpc.id,
                cidr_block=subnet['cidr_block'],
                availability_zone=subnet['availability_zone'],
                map_public_ip_on_launch=subnet['map_public_ip_on_launch']
            )
            subnet_ids.append(sn.id)

            # Create a NAT Gateway in the public subnet
            if subnet['map_public_ip_on_launch']:
                eip = ec2.Eip(f"{subnet['name']}-{self.config.name}-eip")
                nat_gateway = ec2.NatGateway(f"{subnet['name']}-{self.config.name}-nat", subnet_id=sn.id, allocation_id=eip.id)

                # Create a route table for the private subnet
                route_table = ec2.RouteTable(f"{subnet['name']}-{self.config.name}-rt", vpc_id=vpc.id)
                ec2.RouteTableAssociation(f"{subnet['name']}-{self.config.name}-rta", subnet_id=sn.id, route_table_id=route_table.id)
                ec2.Route(f"{subnet['name']}-{self.config.name}-route", route_table_id=route_table.id, destination_cidr_block="0.0.0.0/0", nat_gateway_id=nat_gateway.id)

        # Store outputs
        self.config.outputs['vpc_id'] = vpc.id
        self.config.outputs['subnet_ids'] = subnet_ids

        # Export outputs
        pulumi.export("vpc_id", vpc.id)
        pulumi.export("subnet_ids", subnet_ids)

    def output_dto(self) -> VPCConfigDTO:
        return self.config
