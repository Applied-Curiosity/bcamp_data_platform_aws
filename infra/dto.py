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
