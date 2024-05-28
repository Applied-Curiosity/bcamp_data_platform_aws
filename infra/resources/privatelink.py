# resources/privatelink.py
import pulumi_aws as aws
from dto import PrivateLinkConfigDTO

class PrivateLinkResource:
    def __init__(self, config: PrivateLinkConfigDTO):
        self.config = config
        self.setup_endpoints()

    def setup_endpoints(self):
        for endpoint in self.config.endpoints:
            pl_endpoint = aws.ec2.VpcEndpoint(
                f"{endpoint['service_name']}-endpoint",
                vpc_id=endpoint['vpc_id'],
                service_name=endpoint['service_name'],
                subnet_ids=endpoint['subnet_ids'],
                security_group_ids=endpoint['security_group_ids'],
                vpc_endpoint_type="Interface"
            )
            # Store output
            if 'endpoint_ids' not in self.config.outputs:
                self.config.outputs['endpoint_ids'] = []
            self.config.outputs['endpoint_ids'].append(pl_endpoint.id)

    def output_dto(self) -> PrivateLinkConfigDTO:
        return self.config
