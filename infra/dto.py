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


# Unified DTO class for entire configuration
@dataclass
class ConfigDTO:
    iam: IAMConfigDTO

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            iam=IAMConfigDTO(**config['iam'])
        )
