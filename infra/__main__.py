# __main__.py
import pulumi
import yaml
import json
from dto import ConfigDTO

# Import resource classes
from resources.iam import IAMResource
from resources.storage import S3Resource
from resources.vpc import VPCResource
from resources.security import SecurityResource
# from resources.databricks import DatabricksResource
from resources.privatelink import PrivateLinkResource
from resources.kms import KMSResource
# from resources.bastion import BastionResource

# Load configuration based on the current Pulumi stack
stack = pulumi.get_stack()
config_path = f'config/{stack}.yml'

with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

# Create DTOs from configuration
config_dto = ConfigDTO.from_dict(config_data)

# Instantiate resources with DTO
iam_resource = IAMResource(config_dto.iam)
storage_resource = S3Resource(config_dto.storage)

# Creating VPC resource and getting the VPC ID
vpc_resource = VPCResource(config_dto.vpc)
vpc_outputs = vpc_resource.output_dto().outputs
vpc_id = vpc_outputs['vpc_id']
subnet_id = vpc_outputs['subnet_ids'][0]  # Corrected key here

# Instantiate security resource and pass the VPC ID to the security resource
security_resource = SecurityResource(config_dto.security, vpc_id)
security_outputs = security_resource.output_dto().outputs
sg_id = security_outputs['security_group_ids'][0]

databricks_resource = DatabricksResource(config_dto.databricks)

# Instantiate the PrivateLink resource
privatelink_config = config_dto.privatelink
for endpoint in privatelink_config.endpoints:
    endpoint['vpc_id'] = vpc_id
    endpoint['subnet_ids'] = [subnet_id]
    endpoint['security_group_ids'] = [sg_id]
privatelink_resource = PrivateLinkResource(config_dto.privatelink)

# Instantiate the KMS resource
kms_resource = KMSResource(config_dto.kms)

# Bastion resource
# bastion_resource = BastionResource(config_dto.bastion)

# Export any necessary outputs
pulumi.export('iam_outputs', iam_resource.output_dto().outputs)
pulumi.export('S3_outputs', storage_resource.output_dto().outputs)
pulumi.export('VPC_outputs', vpc_outputs)
pulumi.export('Security_outputs', security_outputs)
pulumi.export('databricks_outputs', databricks_resource.output_dto().outputs)
pulumi.export('privatelink_outputs', privatelink_resource.output_dto().outputs)
pulumi.export('kms_outputs', kms_resource.output_dto().outputs)