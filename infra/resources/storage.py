# resources/storage.py
import pulumi_aws as aws
from dto import StorageConfigDTO

class S3Resource:
    def __init__(self, config: StorageConfigDTO):
        self.config = config
        self.create_buckets()

    def create_buckets(self):
        for bucket_config in self.config.s3_buckets:
            bucket = aws.s3.Bucket(
                bucket_config['name'],
                acl="private",
                tags={"Environment": "dev"},
                versioning=aws.s3.BucketVersioningArgs(
                    enabled=bucket_config['versioning']
                ),
                server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
                    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
                        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                            sse_algorithm=bucket_config['server_side_encryption']
                        )
                    )
                )
            )
            # Optionally set up logging
            # if bucket_config.logging:
            #     aws.s3.BucketLogging(
            #         f"{bucket_config.name}-logging",
            #         bucket=bucket.id,
            #         target_bucket=bucket_config['logging']['target_bucket'],
            #         target_prefix=bucket_config['logging']['target_prefix']
            #     )
            # Store outputs
            if 'bucket_arns' not in self.config.outputs:
                self.config.outputs['bucket_arns'] = []
            if 'bucket_names' not in self.config.outputs:
                self.config.outputs['bucket_names'] = []
            self.config.outputs['bucket_arns'].append(bucket.arn)
            self.config.outputs['bucket_names'].append(bucket.id)

    def output_dto(self) -> StorageConfigDTO:
        return self.config
