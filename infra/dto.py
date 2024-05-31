from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Define individual configuration classes for each resource type
# @dataclass
# class IAMConfig:
#     roles: List[Dict[str, any]]
#     outputs: Dict[str, List[str]] = field(default_factory=dict)

#IAM Role Class
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

# Storage Bucket
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

# VPC
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


# DataBricks Workspace DTO
@dataclass
class DatabricksWorkspaceConfig:
    name: str
    region: str
    sku: str
    managed_resource_group_id: str
    network: Dict[str, List[str]]  # Network settings including VPC, subnets, and security groups

@dataclass
class DatabricksConfigDTO:
    workspace: DatabricksWorkspaceConfig
    outputs: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'DatabricksConfigDTO':
        return DatabricksConfigDTO(
            workspace=DatabricksWorkspaceConfig(**config['workspace']),
            outputs=config.get('outputs', {})
        )


# Privatelink DTO class
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

# AWS KMS DTO
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

# Unified DTO class for entire configuration
@dataclass
class ConfigDTO:
    iam: IAMConfigDTO
    storage: StorageConfigDTO
    vpc: VPCConfigDTO
    security: SecurityConfigDTO
    databricks: DatabricksConfigDTO
    privatelink: PrivateLinkConfigDTO
    kms: KMSConfigDTO

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(

            iam=IAMConfigDTO(**config['iam']),
            storage=StorageConfigDTO(**config['storage']),
            vpc=VPCConfigDTO(**config['vpc']),
            security=SecurityConfigDTO(**config['security']),
            databricks=DatabricksConfigDTO(**config['databricks']),
            privatelink=PrivateLinkConfigDTO(**config['privatelink']),
            kms=KMSConfigDTO(**config['kms']),
        )
