# YAML Configuration for KMS
kms:
  keys:
    - alias: "alias/myapp-key"
      description: "Encryption key for myapp"
      policy: |
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
              "Action": "kms:*",
              "Resource": "*"
            }
          ]
        }
  outputs:
    key_ids: []
    key_arns: []

# resources/kms.py
import pulumi_aws as aws
from dto import KMSConfigDTO

class KMSResource:
    def __init__(self, config: KMSConfigDTO):
        self.config = config
        self.setup_keys()

    def setup_keys(self):
        for key_config in self.config.keys:
            key = aws.kms.Key(
                key_config.alias,
                description=key_config.description,
                policy=key_config.policy
            )
            # Alias for the key
            aws.kms.Alias(
                key_config.alias,
                target_key_id=key.id,
                name=key_config.alias
            )
            # Store output
            if 'key_ids' not in self.config.outputs:
                self.config.outputs['key_ids'] = []
            if 'key_arns' not in self.config.outputs:
                self.config.outputs['key_arns'] = []
            self.config.outputs['key_ids'].append(key.id)
            self.config.outputs['key_arns'].append(key.arn)

    def output_dto(self) -> KMSConfigDTO:
        return self.config
