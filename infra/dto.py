from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Define the common tagging data class
@dataclass
class CommonTags:
    Environment: str
    Project: str
    Owner: str
    Team: str
    CostCenter: str
    Lifecycle: str
    Application: Optional[str] = None
    Purpose: Optional[str] = None
    Compliance: Optional[str] = None
    ManagedBy: Optional[str] = None

    def to_dict(self):
        return {
            "Environment": self.Environment,
            "Project": self.Project,
            "Owner": self.Owner,
            "Team": self.Team,
            "CostCenter": self.CostCenter,
            "Lifecycle": self.Lifecycle,
            "Application": self.Application,
            "Purpose": self.Purpose,
            "Compliance": self.Compliance,
            "ManagedBy": self.ManagedBy
        }

# IAM Role Class
@dataclass
class IAMRoleConfig:
    name: str
    assume_role_policy: str
    policies: List[str]
    tags: CommonTags

@dataclass
class IAMConfigDTO:
    roles: List[IAMRoleConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'IAMConfigDTO':
        roles = [IAMRoleConfig(**role, tags=common_tags) for role in config['roles']]
        outputs = config.get('outputs', {})
        return IAMConfigDTO(roles=roles, outputs=outputs)

# Storage Bucket
@dataclass
class S3BucketConfig:
    name: str
    region: str
    public_access_block: bool
    versioning: bool
    logging: Optional[Dict[str, str]]
    server_side_encryption: str
    tags: CommonTags

@dataclass
class StorageConfigDTO:
    s3_buckets: List[S3BucketConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'StorageConfigDTO':
        buckets = [S3BucketConfig(**bucket, tags=common_tags) for bucket in config['s3_buckets']]
        outputs = config.get('outputs', {})
        return StorageConfigDTO(s3_buckets=buckets, outputs=outputs)

# VPC
@dataclass
class SubnetConfig:
    name: str
    cidr_block: str
    availability_zone: str
    map_public_ip_on_launch: bool
    tags: CommonTags

@dataclass
class VPCConfigDTO:
    name: str
    cidr_block: str
    subnets: List[SubnetConfig]
    internet_gateway: bool
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'VPCConfigDTO':
        subnets = [SubnetConfig(**subnet, tags=common_tags) for subnet in config['subnets']]
        return VPCConfigDTO(
            name=config['name'],
            cidr_block=config['cidr_block'],
            subnets=subnets,
            internet_gateway=config['internet_gateway'],
            outputs=config.get('outputs', {})
        )

# Security
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
    tags: CommonTags

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
    tags: CommonTags
@dataclass
class SecurityConfigDTO:
    security_groups: List[SecurityGroupConfig]
    network_acls: List[NetworkAclConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'SecurityConfigDTO':
        security_groups = [SecurityGroupConfig(**sg, tags=common_tags) for sg in config['security_groups']]
        network_acls = [NetworkAclConfig(**acl, tags=common_tags) for acl in config['network_acls']]
        outputs = config.get('outputs', {})
        return SecurityConfigDTO(security_groups=security_groups, network_acls=network_acls, outputs=outputs)

# Databricks Workspace DTO
@dataclass
class DatabricksWorkspaceConfig:
    name: str
    region: str
    sku: str
    managed_resource_group_id: str
    network: Dict[str, List[str]]  # Network settings including VPC, subnets, and security groups
    tags: CommonTags

@dataclass
class DatabricksConfigDTO:
    workspace: DatabricksWorkspaceConfig
    outputs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'DatabricksConfigDTO':
        return DatabricksConfigDTO(
            workspace=DatabricksWorkspaceConfig(**config['workspace'], tags=common_tags),
            outputs=config.get('outputs', {})
        )

# Privatelink DTO class
@dataclass
class PrivateLinkEndpointConfig:
    service_name: str
    vpc_id: str
    subnet_ids: List[str]
    security_group_ids: List[str]
    tags: CommonTags

@dataclass
class PrivateLinkConfigDTO:
    endpoints: List[PrivateLinkEndpointConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'PrivateLinkConfigDTO':
        endpoints = [PrivateLinkEndpointConfig(**ep, tags=common_tags) for ep in config['endpoints']]
        outputs = config.get('outputs', {})
        return PrivateLinkConfigDTO(endpoints=endpoints, outputs=outputs)

# AWS KMS DTO
@dataclass
class KMSKeyConfig:
    alias: str
    description: str
    policy: str
    tags: CommonTags

@dataclass
class KMSConfigDTO:
    keys: List[KMSKeyConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'KMSConfigDTO':
        keys = [KMSKeyConfig(**key, tags=common_tags) for key in config['keys']]
        outputs = config.get('outputs', {})
        return KMSConfigDTO(keys=keys, outputs=outputs)

'''
@dataclass
class BastionInstanceConfig:
    name: str
    ami: str
    instance_type: str
    key_name: str
    vpc_security_group_ids: List[str]
    subnet_id: str
    associate_public_ip_address: bool
    tags: CommonTags

@dataclass
class BastionConfigDTO:
    instance: BastionInstanceConfig
    outputs: dict = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict, common_tags: CommonTags) -> 'BastionConfigDTO':
        return BastionConfigDTO(
            instance=BastionInstanceConfig(**config['instance'], tags=common_tags),
            outputs=config.get('outputs', {})
        )
'''
# Unified DTO class for entire configuration
@dataclass
class ConfigDTO:
    common_tags: CommonTags
    iam: IAMConfigDTO
    storage: StorageConfigDTO
    vpc: VPCConfigDTO
    security: SecurityConfigDTO
    databricks: DatabricksConfigDTO
    privatelink: PrivateLinkConfigDTO
    kms: KMSConfigDTO
    # bastion: BastionConfigDTO

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        common_tags = CommonTags(**config['common_tags'])
        return ConfigDTO(
            common_tags=common_tags,
            iam=IAMConfigDTO.from_dict(config['iam'], common_tags),
            storage=StorageConfigDTO.from_dict(config['storage'], common_tags),
            vpc=VPCConfigDTO.from_dict(config['vpc'], common_tags),
            security=SecurityConfigDTO.from_dict(config['security'], common_tags),
            databricks=DatabricksConfigDTO.from_dict(config['databricks'], common_tags),
            privatelink=PrivateLinkConfigDTO.from_dict(config['privatelink'], common_tags),
            kms=KMSConfigDTO.from_dict(config['kms'], common_tags),
            # bastion=BastionConfigDTO.from_dict(config['bastion'], common_tags),
        )
