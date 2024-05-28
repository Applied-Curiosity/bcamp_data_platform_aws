# resources/kms.py
import json
import pulumi_aws as aws
from dto import KMSConfigDTO

class KMSResource:
    def __init__(self, config: KMSConfigDTO):
        self.config = config
        self.setup_keys()

    def setup_keys(self):
        self.key_ids = []
        self.key_arns = []

        for key_config in self.config.keys:
            key_policy = key_config['policy']
            kms_key = aws.kms.Key(
                key_config['alias'],
                description=key_config['description'],
                policy=key_policy
            )

            # Create an alias for the key
            alias = aws.kms.Alias(
                key_config['alias'],
                target_key_id=kms_key.id
            )

            # Store outputs
            self.key_ids.append(kms_key.id)
            self.key_arns.append(kms_key.arn)

        self.config.outputs['key_ids'] = self.key_ids
        self.config.outputs['key_arns'] = self.key_arns

    def output_dto(self) -> KMSConfigDTO:
        return self.config
