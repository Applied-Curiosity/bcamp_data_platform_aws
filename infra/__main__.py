import pulumi
from dto import ConfigDTO
import yaml
import os

# Import resource classes
from resources.iam import IAMResource

from resources.vpc import VPCResource
from resources.security import SecurityResource
from resources.storage import S3Resource
from resources.databricks import DatabricksResource
from resources.privatelink import PrivateLinkResource
from resources.kms import KMSResource
from resources.monitoring import MonitoringResource
from resources.bastion import BastionResource
from resources.connectivity import ConnectivityResource
from resources.compliance import ComplianceResource

# Load configuration based on the current Pulumi stack
stack = pulumi.get_stack()
config_path = f'config/{stack}.yml'

with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

# Create DTOs from configuration
config_dto = ConfigDTO.from_dict(config_data)

# Instantiate resources with DTO
iam_resource = IAMResource(config_dto.iam)
vpc_resource = VPCResource(config_dto.vpc)
security_resource = SecurityResource(config_dto.security)
storage_resource = S3Resource(config_dto.storage)
databricks_resource = DatabricksResource(config_dto.databricks)
privatelink_resource = PrivateLinkResource(config_dto.privatelink)
kms_resource = KMSResource(config_dto.kms)
monitoring_resource = MonitoringResource(config_dto.monitoring)
bastion_resource = BastionResource(config_dto.bastion)
connectivity_resource = ConnectivityResource(config_dto.connectivity)
compliance_resource = ComplianceResource(config_dto.compliance)

# Export any necessary outputs
pulumi.export('iam_outputs', iam_resource.output_dto().outputs)
pulumi.export('vpc_outputs', vpc_resource.output_dto().outputs)
pulumi.export('security_outputs', security_resource.output_dto().outputs)
pulumi.export('storage_outputs', storage_resource.output_dto().outputs)
pulumi.export('databricks_outputs', databricks_resource.output_dto().outputs)
pulumi.export('privatelink_outputs', privatelink_resource.output_dto().outputs)
pulumi.export('kms_outputs', kms_resource.output_dto().outputs)
pulumi.export('monitoring_outputs', monitoring_resource.output_dto().outputs)
pulumi.export('bastion_outputs', bastion_resource.output_dto().outputs)
pulumi.export('connectivity_outputs', connectivity_resource.output_dto().outputs)
pulumi.export('compliance_outputs', compliance_resource.output_dto().outputs)
