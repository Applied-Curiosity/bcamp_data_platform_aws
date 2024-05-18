# DTO Class Definition for IAM
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class IAMRoleConfig:
    name: str
    assume_role_policy: str
    policies: List[str]

@dataclass
class IAMConfigDTO:
    roles: List[IAMRoleConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'IAMConfigDTO':
        roles = [IAMRoleConfig(**role) for role in config['roles']]
        outputs = config.get('outputs', {})
        return IAMConfigDTO(roles=roles, outputs=outputs)

# DTO Class Definition for VPC
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class SubnetConfig:
    name: str
    cidr_block: str
    availability_zone: str
    map_public_ip_on_launch: bool

@dataclass
class VPCConfigDTO:
    name: str
    cidr_block: str
    subnets: List[SubnetConfig]
    internet_gateway: bool
    nat_gateways: List[Dict[str, str]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'VPCConfigDTO':
        subnets = [SubnetConfig(**subnet) for subnet in config['subnets']]
        nat_gateways = config.get('nat_gateways', [])
        return VPCConfigDTO(
            name=config['name'],
            cidr_block=config['cidr_block'],
            subnets=subnets,
            internet_gateway=config['internet_gateway'],
            nat_gateways=nat_gateways,
            outputs=config.get('outputs', {})
        )

# DTO Class Definition for Security
# dto.py
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class IngressEgressRule:
    protocol: str
    from_port: int
    to_port: int
    cidr_blocks: List[str]

@dataclass
class SecurityGroupConfig:
    name: str
    description: str
    vpc_id: str
    ingress: List[IngressEgressRule]
    egress: List[IngressEgressRule]

@dataclass
class NetworkAclRule:
    rule_number: int
    protocol: str
    rule_action: str
    cidr_block: str
    from_port: int
    to_port: int

@dataclass
class NetworkAclConfig:
    name: str
    vpc_id: str
    ingress: List[NetworkAclRule]
    egress: List[NetworkAclRule]

@dataclass
class SecurityConfigDTO:
    security_groups: List[SecurityGroupConfig]
    network_acls: List[NetworkAclConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

# DTO Class Definition for Storage
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class S3BucketConfig:
    name: str
    region: str
    public_access_block: bool
    versioning: bool
    logging: Optional[Dict[str, str]]
    server_side_encryption: str

@dataclass
class StorageConfigDTO:
    s3_buckets: List[S3BucketConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'StorageConfigDTO':
        buckets = [S3BucketConfig(**bucket) for bucket in config['s3_buckets']]
        outputs = config.get('outputs', {})
        return StorageConfigDTO(s3_buckets=buckets, outputs=outputs)

# DTO Class Definition for Databricks
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class DatabricksWorkspaceConfig:
    name: str
    region: str
    sku: str
    managed_resource_group_id: str
    network: Dict[str, List[str] or str]  # Network settings including VPC, subnets, and security groups

@dataclass
class DatabricksConfigDTO:
    workspace: DatabricksWorkspaceConfig
    outputs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'DatabricksConfigDTO':
        return DatabricksConfigDTO(
            workspace=DatabricksWorkspaceConfig(**config['workspace']),
            outputs=config.get('outputs', {})

# DTO Class Definition for PrivateLink
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class PrivateLinkEndpointConfig:
    service_name: str
    vpc_id: str
    subnet_ids: List[str]
    security_group_ids: List[str]

@dataclass
class PrivateLinkConfigDTO:
    endpoints: List[PrivateLinkEndpointConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'PrivateLinkConfigDTO':
        endpoints = [PrivateLinkEndpointConfig(**ep) for ep in config['endpoints']]
        outputs = config.get('outputs', {})
        return PrivateLinkConfigDTO(endpoints=endpoints, outputs=outputs)

# DTO Class Definition for KMS
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class KMSKeyConfig:
    alias: str
    description: str
    policy: str

@dataclass
class KMSConfigDTO:
    keys: List[KMSKeyConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'KMSConfigDTO':
        keys = [KMSKeyConfig(**key) for key in config['keys']]
        outputs = config.get('outputs', {})
        return KMSConfigDTO(keys=keys, outputs=outputs)

# DTO Class Definition for Monitoring
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CloudTrailConfig:
    name: str
    s3_bucket_name: str
    include_global_service_events: bool
    is_multi_region_trail: bool
    enable_log_file_validation: bool

@dataclass
class CloudWatchConfig:
    log_group_name: str
    retention_in_days: int

@dataclass
class MonitoringConfigDTO:
    cloudtrail: CloudTrailConfig
    cloudwatch: CloudWatchConfig
    outputs: dict = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'MonitoringConfigDTO':
        return MonitoringConfigDTO(
            cloudtrail=CloudTrailConfig(**config['cloudtrail']),
            cloudwatch=CloudWatchConfig(**config['cloudwatch']),
            outputs=config.get('outputs', {})
        )
# DTO Class Definition for Bastion Host
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class BastionInstanceConfig:
    name: str
    ami: str
    instance_type: str
    key_name: str
    vpc_security_group_ids: List[str]
    subnet_id: str
    associate_public_ip_address: bool

@dataclass
class BastionConfigDTO:
    instance: BastionInstanceConfig
    outputs: dict = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'BastionConfigDTO':
        return BastionConfigDTO(
            instance=BastionInstanceConfig(**config['instance']),
            outputs=config.get('outputs', {})
        )

# DTO Class Definition for Connectivity
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class VPCPeeringConfig:
    peering_name: str
    source_vpc_id: str
    target_vpc_id: str
    auto_accept: bool

@dataclass
class TransitGatewayConfig:
    gateway_name: str
    description: str
    default_route_table_association: str
    default_route_table_propagation: str
    auto_accept_shared_attachments: str

@dataclass
class ConnectivityConfigDTO:
    vpc_peering: List[VPCPeeringConfig]
    transit_gateway: List[TransitGatewayConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'ConnectivityConfigDTO':
        vpc_peering = [VPCPeeringConfig(**peer) for peer in config['vpc_peering']]
        transit_gateway = [TransitGatewayConfig(**gateway) for gateway in config['transit_gateway']]
        outputs = config.get('outputs', {})
        return ConnectivityConfigDTO(vpc_peering=vpc_peering, transit_gateway=transit_gateway, outputs=outputs)

# DTO Class Definition for Compliance
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class TaggingPolicy:
    required_tags: List[str]

@dataclass
class EncryptionPolicy:
    enforce_on: List[str]

@dataclass
class AuditSettings:
    trail_name: str
    log_bucket: str

@dataclass
class ComplianceConfigDTO:
    enforce_tagging: TaggingPolicy
    encryption_policies: EncryptionPolicy
    audit_settings: AuditSettings
    outputs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'ComplianceConfigDTO':
        return ComplianceConfigDTO(
            enforce_tagging=TaggingPolicy(**config['enforce_tagging']),
            encryption_policies=EncryptionPolicy(**config['encryption_policies']),
            audit_settings=AuditSettings(**config['audit_settings']),
            outputs=config.get('outputs', {})
        )
# COMPLETE DTO
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Define individual configuration classes for each resource type
@dataclass
class IAMConfig:
    roles: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class VPCConfig:
    name: str
    cidr: str
    subnets: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class SecurityConfig:
    security_groups: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class StorageConfig:
    buckets: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class DatabricksConfig:
    workspace: Dict[str, any]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class PrivateLinkConfig:
    endpoints: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class KMSConfig:
    keys: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class MonitoringConfig:
    cloudtrail: Dict[str, any]
    cloudwatch: Dict[str, any]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class BastionConfig:
    instance: Dict[str, any]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class ConnectivityConfig:
    peering_connections: List[Dict[str, any]]
    transit_gateways: List[Dict[str, any]]
    outputs: Dict[str, List[str]] = field

(default_factory=dict)

@dataclass
class ComplianceConfig:
    policies: Dict[str, any]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

# Unified DTO class for entire configuration
@dataclass
class ConfigDTO:
    iam: IAMConfig
    vpc: VPCConfig
    security: SecurityConfig
    storage: StorageConfig
    databricks: DatabricksConfig
    privatelink: PrivateLinkConfig
    kms: KMSConfig
    monitoring: MonitoringConfig
    bastion: BastionConfig
    connectivity: ConnectivityConfig
    compliance: ComplianceConfig

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            iam=IAMConfig(**config['iam']),
            vpc=VPCConfig(**config['vpc']),
            security=SecurityConfig(**config['security']),
            storage=StorageConfig(**config['storage']),
            databricks=DatabricksConfig(**config['databricks']),
            privatelink=PrivateLinkConfig(**config['privatelink']),
            kms=KMSConfig(**config['kms']),
            monitoring=MonitoringConfig(**config['monitoring']),
            bastion=BastionConfig(**config['bastion']),
            connectivity=ConnectivityConfig(**config['connectivity']),
            compliance=ComplianceConfig(**config['compliance'])
        )
